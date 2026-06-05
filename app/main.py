from fastapi import FastAPI, HTTPException

from app import services
from app.models import Deployment, DeploymentListResponse, DeploymentService, DeploymentStatus

app = FastAPI(title="Deployment API")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/deployments", response_model=DeploymentListResponse)
def list_deployments(
    service: DeploymentService | None = None,
    status: DeploymentStatus | None = None,
):
    deployments = services.list_deployments(service=service, status=status)

    return DeploymentListResponse(count=len(deployments), data=deployments)


@app.get("/deployments/{deployment_id}", response_model=Deployment)
def get_deployment(deployment_id: str):
    deployment = services.get_deployment_by_id(deployment_id)

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found",
        )

    return deployment
