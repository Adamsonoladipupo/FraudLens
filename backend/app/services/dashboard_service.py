from app.repositories.dashboard_repository import (
    DashboardRepository,
)


class DashboardService:

    def __init__(
            self,
            repository: DashboardRepository,
    ) -> None:
        self.repository = repository

    def get_statistics(self):
        return self.repository.get_statistics()