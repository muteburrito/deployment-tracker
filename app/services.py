from app.models import DeploymentService, DeploymentStatus
from app.repository import DeploymentRepository

repo = DeploymentRepository()


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
