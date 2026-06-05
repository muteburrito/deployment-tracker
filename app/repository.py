from app.seed_data import DEPLOYMENTS


class DeploymentRepository:

    def get_all(self):
        return DEPLOYMENTS

    def get_by_id(self, deployment_id: str):
        for deployment in DEPLOYMENTS:
            if deployment.id == deployment_id:
                return deployment

        return None
