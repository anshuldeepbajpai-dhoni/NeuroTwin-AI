import logging
from difflib import SequenceMatcher

from sqlalchemy.orm import Session

from app.crud.memory import create_memory
from app.models.memory import Memory
from app.models.user import User
from app.schemas.memory import MemoryCreate
from app.services.memory_extractor import (
    memory_extractor,
)


logger = logging.getLogger(__name__)


class AutomaticMemoryService:
    """
    Extract, create, update, and prevent
    duplicate long-term memories.
    """

    DUPLICATE_THRESHOLD = 0.85

    UPDATE_THRESHOLD = 0.55

    def process_message(
        self,
        db: Session,
        current_user: User,
        user_message: str,
    ):
        """
        Extract useful information and
        create, update, or skip a memory.
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

            matching_memory, similarity = (
                self.find_matching_memory(
                    db=db,
                    user_id=current_user.id,
                    title=extracted_memory[
                        "title"
                    ],
                    content=extracted_memory[
                        "content"
                    ],
                    category=extracted_memory[
                        "category"
                    ],
                )
            )

            if (
                matching_memory
                and similarity
                >= self.DUPLICATE_THRESHOLD
            ):
                logger.info(
                    "Duplicate memory skipped "
                    "for user %s.",
                    current_user.id,
                )

                return matching_memory

            if (
                matching_memory
                and similarity
                >= self.UPDATE_THRESHOLD
            ):
                return self.update_memory(
                    db=db,
                    memory=matching_memory,
                    extracted_memory=(
                        extracted_memory
                    ),
                )

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

    def find_matching_memory(
        self,
        db: Session,
        user_id: str,
        title: str,
        content: str,
        category: str,
    ) -> tuple[
        Memory | None,
        float,
    ]:
        """
        Find the user's most similar memory
        in the same category.
        """

        existing_memories = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.category == category,
            )
            .all()
        )

        new_title = self.normalize_text(
            title
        )

        new_content = self.normalize_text(
            content
        )

        best_memory = None

        best_similarity = 0.0

        for memory in existing_memories:

            title_similarity = (
                SequenceMatcher(
                    None,
                    new_title,
                    self.normalize_text(
                        memory.title
                    ),
                ).ratio()
            )

            content_similarity = (
                SequenceMatcher(
                    None,
                    new_content,
                    self.normalize_text(
                        memory.content
                    ),
                ).ratio()
            )

            similarity = max(
                title_similarity,
                content_similarity,
            )

            if similarity > best_similarity:

                best_similarity = similarity

                best_memory = memory

        return (
            best_memory,
            best_similarity,
        )

    @staticmethod
    def update_memory(
        db: Session,
        memory: Memory,
        extracted_memory: dict,
    ) -> Memory:
        """
        Replace an existing memory with
        newer extracted information.
        """

        memory.title = (
            extracted_memory["title"]
        )

        memory.content = (
            extracted_memory["content"]
        )

        memory.category = (
            extracted_memory["category"]
        )

        memory.importance = (
            extracted_memory["importance"]
        )

        db.commit()

        db.refresh(
            memory
        )

        return memory

    @staticmethod
    def normalize_text(
        value: str,
    ) -> str:
        """
        Normalize text before similarity
        comparison.
        """

        return " ".join(
            value.lower()
            .strip()
            .split()
        )


automatic_memory_service = (
    AutomaticMemoryService()
)