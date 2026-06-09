from datetime import datetime
from typing import Literal

from pydantic import BaseModel

DeploymentStatus = Literal["success", "failed", "running", "cancelled"]
DeploymentService = Literal[
    "auth-service",
    "billing-api",
    "checkout-api",
    "deployments-ui",
    "notification-worker",
]


class Deployment(BaseModel):
    id: str
    service: DeploymentService
    status: DeploymentStatus
    duration: int
    timestamp: datetime
    commit_sha: str


class DeploymentListResponse(BaseModel):
    count: int
    data: list[Deployment]


class DeploymentMetrics(BaseModel):
    service: DeploymentService
    deployment_frequency: float
    failure_rate: float
    p95_duration: int


class DeploymentMetricsResponse(BaseModel):
    count: int
    data: list[DeploymentMetrics]
