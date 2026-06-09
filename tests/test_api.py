import pytest

from datetime import datetime
from fastapi import HTTPException
from pydantic import ValidationError

from app.main import get_deployment, get_metrics, list_deployments
from app.models import Deployment


def test_list_deployments_returns_data():
    response = list_deployments()

    assert len(response.data) >= 45
    assert response.count == len(response.data)
    assert all(item.timestamp.year == 2026 for item in response.data)
    assert all(item.timestamp.month == 5 for item in response.data)
    assert min(item.timestamp.day for item in response.data) == 1
    assert max(item.timestamp.day for item in response.data) == 31


def test_list_deployments_filters_by_service_and_status():
    response = list_deployments(service="billing-api", status="failed")

    assert response.count == 2
    assert all(item.service == "billing-api" for item in response.data)
    assert all(item.status == "failed" for item in response.data)


def test_deployment_rejects_unknown_service():
    with pytest.raises(ValidationError):
        Deployment(
            id="deploy_unknown",
            service="unknown-service",
            status="success",
            duration=100,
            timestamp=datetime.fromisoformat("2026-05-01T00:00:00Z"),
            commit_sha="abc123",
        )


def test_get_deployment_returns_details():
    response = get_deployment("deploy_001")

    assert response.id == "deploy_001"


def test_get_unknown_deployment_returns_404():
    with pytest.raises(HTTPException) as exc_info:
        get_deployment("deploy_999")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Deployment not found"


def test_get_metrics_returns_service_metrics_for_time_range():
    response = get_metrics(time_range="31d")

    assert response.count == 5

    metrics_by_service = {
        item.service: item
        for item in response.data
    }

    billing_metrics = metrics_by_service["billing-api"]
    assert billing_metrics.deployment_frequency == pytest.approx(9 / 31)
    assert billing_metrics.failure_rate == pytest.approx(3 / 8)
    assert billing_metrics.p95_duration == 415


def test_get_metrics_filters_to_trailing_time_range():
    response = get_metrics(time_range="7d")

    assert response.count == 5
    assert all(item.deployment_frequency == pytest.approx(1 / 7) for item in response.data)
    assert all(item.failure_rate == 0 for item in response.data)


def test_get_metrics_returns_grouped_metrics():
    response = get_metrics(time_range="31d")

    assert {
        item.service
        for item in response.data
    } == {
        "auth-service",
        "billing-api",
        "checkout-api",
        "deployments-ui",
        "notification-worker",
    }


def test_get_metrics_rejects_invalid_time_range():
    with pytest.raises(HTTPException) as exc_info:
        get_metrics(time_range="seven-days")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "time_range must be a positive number of days, such as 7d"


def test_get_metrics_requires_time_range():
    with pytest.raises(HTTPException) as exc_info:
        get_metrics()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "time_range is required"
