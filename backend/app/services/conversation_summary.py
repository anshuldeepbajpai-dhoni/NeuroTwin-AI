import logging

from sqlalchemy.orm import Session

from app.models.conversation import (
    Conversation,
)
from app.services.conversation_summarizer import (
    conversation_summarizer,
)


logger = logging.getLogger(__name__)


class ConversationSummaryService:
    """
    Generate and store summaries for
    sufficiently long conversations.
    """

    def update_summary(
        self,
        db: Session,
        conversation: Conversation,
        messages: list,
    ) -> str | None:
        """
        Generate and store a summary when
        enough conversation messages exist.
        """

        try:
            summary = (
                conversation_summarizer
                .summarize(
                    messages
                )
            )

            if summary is None:
                return None

            conversation.summary = summary

            db.commit()

            db.refresh(
                conversation
            )

            return summary

        except Exception as error:
            db.rollback()

            logger.warning(
                "Conversation summary update "
                "failed: %s",
                error,
            )

            return None


conversation_summary_service = (
    ConversationSummaryService()
)