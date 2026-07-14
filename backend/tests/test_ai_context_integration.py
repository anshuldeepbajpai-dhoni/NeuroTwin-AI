from types import SimpleNamespace
from unittest.mock import MagicMock
from unittest.mock import patch

from app.services.ai_context import (
    ai_context_builder,
)


@patch(
    "app.services.ai_context."
    "conversation_context_builder."
    "build_context"
)
@patch(
    "app.services.ai_context."
    "memory_context_builder."
    "build_context"
)
@patch(
    "app.services.ai_context."
    "prompt_builder."
    "build_system_prompt"
)
def test_complete_ai_context_is_built(
    mock_build_system_prompt,
    mock_memory_context,
    mock_conversation_context,
):
    """
    Verify that the complete AI context
    contains the Digital Twin prompt,
    relevant memories, and recent
    conversation history.
    """

    db = MagicMock()

    digital_twin = SimpleNamespace(
        id="test-digital-twin-id",
    )

    mock_build_system_prompt.return_value = (
        "You are Anshul's personalized "
        "AI Digital Twin. Be practical, "
        "clear, and supportive."
    )

    mock_memory_context.return_value = (
        "- Goal: Become an AI engineer.\n"
        "- Interest: Python and FastAPI."
    )

    conversation_history = [
        {
            "role": "user",
            "content": (
                "I am learning FastAPI."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "FastAPI is useful for "
                "building production APIs."
            ),
        },
    ]

    mock_conversation_context.return_value = (
        conversation_history
    )

    result = (
        ai_context_builder.build_context(
            db=db,
            digital_twin=digital_twin,
            conversation_id=(
                "test-conversation-id"
            ),
            user_id="test-user-id",
        )
    )

    print(
        "\nBUILT AI CONTEXT:"
    )

    for index, message in enumerate(
        result
    ):
        print(
            index,
            message,
        )

    assert isinstance(
        result,
        list,
    )

    assert (
        len(result)
        == 2 + len(
            conversation_history
        )
    )

    system_message = result[0]

    assert (
        system_message["role"]
        == "system"
    )

    system_content = (
        system_message["content"]
    )

    assert (
        "personalized AI Digital Twin"
        in system_content
    )

    assert (
        "Become an AI engineer"
        in system_content
    )

    assert (
        "Python and FastAPI"
        in system_content
    )

    assert (
        "Use memories only when relevant"
        in system_content
    )

    assert (
        "Do not invent information"
        in system_content
    )

    summary_message = (
        result[1]
    )

    assert (
        summary_message["role"]
        == "system"
    )

    assert (
        "Previous conversation summary:"
        in summary_message["content"]
    )

    assert (
        result[2:]
        == conversation_history
    )

    mock_build_system_prompt\
        .assert_called_once_with(
            digital_twin
        )

    mock_memory_context\
        .assert_called_once_with(
            db=db,
            user_id="test-user-id",
            digital_twin_id=(
                "test-digital-twin-id"
            ),
        )

    mock_conversation_context\
        .assert_called_once_with(
            db=db,
            conversation_id=(
                "test-conversation-id"
            ),
            user_id="test-user-id",
        )