import math
import re
from collections import defaultdict
from datetime import timedelta

from app.models import DeploymentMetrics, DeploymentService, DeploymentStatus
from app.repository import DeploymentRepository

repo = DeploymentRepository()

TIME_RANGE_PATTERN = re.compile(r"^(?P<days>[1-9]\d*)d$")


def list_deployments(
    service: DeploymentService | None = None,
    status: DeploymentStatus | None = None,
):
    deployments = repo.get_all()

    if service:
        deployments = [
            d for d in deployments
            if d.service == service
        ]

    if status:
        deployments = [
            d for d in deployments
            if d.status == status
        ]

    return deployments


def get_deployment_by_id(deployment_id: str):
    return repo.get_by_id(deployment_id)


def get_deployment_metrics(time_range: str | None = None):
    deployments = repo.get_all()

    if not deployments:
        return []

    days = _get_range_days(deployments, time_range)
    latest_timestamp = max(deployment.timestamp for deployment in deployments)
    start_timestamp = latest_timestamp - timedelta(days=days)
    deployments_in_range = [
        deployment for deployment in deployments
        if deployment.timestamp >= start_timestamp
    ]

    deployments_by_service = defaultdict(list)
    for deployment in deployments_in_range:
        deployments_by_service[deployment.service].append(deployment)

    return [
        _build_service_metrics(service, service_deployments, days)
        for service, service_deployments in sorted(deployments_by_service.items())
    ]


def _get_range_days(deployments, time_range: str | None):
    if time_range is None:
        raise ValueError("time_range is required")

    match = TIME_RANGE_PATTERN.match(time_range)
    if not match:
        raise ValueError("time_range must be a positive number of days, such as 7d")

    return int(match.group("days"))


def _build_service_metrics(service, deployments, days):
    deployment_count = len(deployments)
    completed_deployments = [
        deployment for deployment in deployments
        if deployment.status != "running"
    ]
    completed_count = len(completed_deployments)
    failed_count = sum(
        1 for deployment in completed_deployments
        if deployment.status in {"failed", "cancelled"}
    )
    durations = sorted(deployment.duration for deployment in deployments)

    return DeploymentMetrics(
        service=service,
        deployment_frequency=deployment_count / days,
        failure_rate=failed_count / completed_count if completed_count else 0,
        p95_duration=_nearest_rank_percentile(durations, 95),
    )


def _nearest_rank_percentile(values, percentile: int):
    index = math.ceil(percentile / 100 * len(values)) - 1
    return values[index]
