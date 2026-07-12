from types import SimpleNamespace
from unittest.mock import patch

from app.services.conversation_summarizer import (
    conversation_summarizer,
)


def test_prepare_dictionary_messages():

    messages = [
        {
            "role": "user",
            "content": (
                "  I am learning FastAPI.  "
            ),
        },
        {
            "role": "assistant",
            "content": "Great choice.",
        },
        {
            "role": "system",
            "content": "Ignore this.",
        },
        {
            "role": "user",
            "content": "   ",
        },
    ]

    result = (
        conversation_summarizer
        .prepare_messages(
            messages
        )
    )

    assert result == [
        {
            "role": "user",
            "content": (
                "I am learning FastAPI."
            ),
        },
        {
            "role": "assistant",
            "content": "Great choice.",
        },
    ]


def test_prepare_message_objects():

    messages = [
        SimpleNamespace(
            role="user",
            content=(
                "  I am building NeuroTwin.  "
            ),
        ),
        SimpleNamespace(
            role="assistant",
            content=(
                "That is a useful AI project."
            ),
        ),
    ]

    result = (
        conversation_summarizer
        .prepare_messages(
            messages
        )
    )

    assert result == [
        {
            "role": "user",
            "content": (
                "I am building NeuroTwin."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "That is a useful AI project."
            ),
        },
    ]


def test_build_conversation_text():

    messages = [
        {
            "role": "user",
            "content": (
                "I want to become "
                "an AI engineer."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "Continue learning Python."
            ),
        },
    ]

    result = (
        conversation_summarizer
        .build_conversation_text(
            messages
        )
    )

    assert result == (
        "User: I want to become "
        "an AI engineer.\n"
        "Assistant: Continue learning "
        "Python."
    )


@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_min_messages",
    10,
)
def test_short_conversation_is_not_summarized():

    messages = [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi",
        },
    ]

    result = (
        conversation_summarizer
        .summarize(
            messages
        )
    )

    assert result is None


@patch(
    "app.services.conversation_summarizer."
    "ai_provider_service.generate_response"
)
@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_min_messages",
    2,
)
def test_long_conversation_is_summarized(
    mock_generate_response,
):

    messages = [
        {
            "role": "user",
            "content": (
                "I want to become "
                "an AI engineer."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "Learn Python and "
                "machine learning."
            ),
        },
    ]

    mock_generate_response.return_value = (
        "The user wants to become an "
        "AI engineer and is learning "
        "Python and machine learning."
    )

    result = (
        conversation_summarizer
        .summarize(
            messages
        )
    )

    assert result == (
        "The user wants to become an "
        "AI engineer and is learning "
        "Python and machine learning."
    )

    mock_generate_response.assert_called_once()

    ai_messages = (
        mock_generate_response
        .call_args
        .kwargs["messages"]
    )

    assert (
        ai_messages[0]["role"]
        == "system"
    )

    assert (
        ai_messages[1]["role"]
        == "user"
    )

    assert (
        "I want to become an AI engineer."
        in ai_messages[1]["content"]
    )


@patch(
    "app.services.conversation_summarizer."
    "ai_provider_service.generate_response"
)
@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_min_messages",
    2,
)
def test_empty_summary_returns_none(
    mock_generate_response,
):

    mock_generate_response.return_value = (
        "   "
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi",
        },
    ]

    result = (
        conversation_summarizer
        .summarize(
            messages
        )
    )

    assert result is None


@patch(
    "app.services.conversation_summarizer."
    "ai_provider_service.generate_response"
)
@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_min_messages",
    2,
)
def test_ai_failure_returns_none(
    mock_generate_response,
):

    mock_generate_response.side_effect = (
        RuntimeError(
            "AI provider unavailable"
        )
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi",
        },
    ]

    result = (
        conversation_summarizer
        .summarize(
            messages
        )
    )

    assert result is None


@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_max_characters",
    20,
)
@patch(
    "app.services.conversation_summarizer."
    "ai_provider_service.generate_response"
)
@patch(
    "app.services.conversation_summarizer."
    "settings.ai_summary_min_messages",
    2,
)
def test_summary_length_is_limited(
    mock_generate_response,
):

    mock_generate_response.return_value = (
        "This is a very long conversation "
        "summary generated by the AI."
    )

    messages = [
        {
            "role": "user",
            "content": "Message one",
        },
        {
            "role": "assistant",
            "content": "Message two",
        },
    ]

    result = (
        conversation_summarizer
        .summarize(
            messages
        )
    )

    assert result == (
        "This is a very long "
    )

    assert len(result) == 20