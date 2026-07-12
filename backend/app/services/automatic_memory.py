import logging

from sqlalchemy.orm import Session

from app.crud.memory import create_memory
from app.models.user import User
from app.schemas.memory import MemoryCreate
from app.services.memory_extractor import (
    memory_extractor,
)


logger = logging.getLogger(__name__)


class AutomaticMemoryService:
    """
    Extract and automatically save useful
    long-term information from user messages.
    """

    def process_message(
        self,
        db: Session,
        current_user: User,
        user_message: str,
    ):
        """
        Extract useful information from a
        user message and save it as memory.
        """

        try:
            extracted_memory = (
                memory_extractor.extract(
                    user_message
                )
            )

            if not extracted_memory.get(
                "should_save"
            ):
                return None

            memory_data = MemoryCreate(
                title=extracted_memory[
                    "title"
                ],
                content=extracted_memory[
                    "content"
                ],
                category=extracted_memory[
                    "category"
                ],
                importance=extracted_memory[
                    "importance"
                ],
                is_favorite=False,
            )

            return create_memory(
                db=db,
                current_user=current_user,
                memory_data=memory_data,
            )

        except Exception as error:
            logger.warning(
                "Automatic memory processing "
                "failed: %s",
                error,
            )

            return None


automatic_memory_service = (
    AutomaticMemoryService()
)