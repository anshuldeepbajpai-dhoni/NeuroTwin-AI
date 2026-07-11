from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.memory import Memory


class MemoryContextBuilder:
    """
    Loads relevant user memories and converts
    them into context for the AI model.
    """

    @staticmethod
    def get_relevant_memories(
        db: Session,
        user_id: str,
        digital_twin_id: str,
    ) -> list[Memory]:
        """
        Retrieve the most important memories.

        Favorite memories are prioritized first,
        followed by importance and creation date.
        """

        return (
            db.query(
                Memory
            )
            .filter(
                Memory.user_id == user_id,
                Memory.digital_twin_id
                == digital_twin_id,
            )
            .order_by(
                desc(
                    Memory.is_favorite
                ),
                desc(
                    Memory.importance
                ),
                desc(
                    Memory.created_at
                ),
            )
            .limit(
                settings.ai_max_memories
            )
            .all()
        )

    @staticmethod
    def build_memory_context(
        memories: list[Memory],
    ) -> str:
        """
        Convert Memory objects into a
        structured AI-context section.
        """

        if not memories:
            return (
                "No saved user memories "
                "are currently available."
            )

        memory_items = []

        for index, memory in enumerate(
            memories,
            start=1,
        ):
            title = (
                memory.title.strip()
            )

            content = (
                memory.content.strip()
            )

            category = (
                memory.category.strip()
            )

            favorite = (
                "Yes"
                if memory.is_favorite
                else "No"
            )

            memory_items.append(
                (
                    f"Memory {index}\n"
                    f"Title: {title}\n"
                    f"Category: {category}\n"
                    f"Importance: "
                    f"{memory.importance}/10\n"
                    f"Favorite: {favorite}\n"
                    f"Content: {content}"
                )
            )

        return (
            "Relevant saved user memories:\n\n"
            + "\n\n".join(
                memory_items
            )
        )

    def build_context(
        self,
        db: Session,
        user_id: str,
        digital_twin_id: str,
    ) -> str:
        """
        Load relevant memories and build
        the complete memory-context string.
        """

        memories = (
            self.get_relevant_memories(
                db=db,
                user_id=user_id,
                digital_twin_id=(
                    digital_twin_id
                ),
            )
        )

        return self.build_memory_context(
            memories
        )


memory_context_builder = (
    MemoryContextBuilder()
)