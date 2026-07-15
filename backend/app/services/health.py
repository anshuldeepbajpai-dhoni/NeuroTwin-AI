import logging

from sqlalchemy import text
from sqlalchemy.orm import Session


logger = logging.getLogger(
    __name__
)


class HealthService:
    """
    Check the operational health and
    readiness of backend dependencies.
    """

    @staticmethod
    def check_database(
        db: Session,
    ) -> bool:
        """
        Verify that the database can
        execute a lightweight query.
        """

        try:

            db.execute(
                text("SELECT 1")
            )

            return True

        except Exception as error:

            logger.warning(
                "Database readiness "
                "check failed: %s",
                error,
            )

            return False


health_service = (
    HealthService()
)