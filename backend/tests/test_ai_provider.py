from unittest.mock import patch

import pytest

from app.services.ai_provider import (
    ai_provider_service,
)


def test_ai_provider_rejects_empty_messages():

    with pytest.raises(
        ValueError,
        match="Messages cannot be empty.",
    ):

        ai_provider_service.generate_response(
            messages=[]
        )


@patch(
    "app.services.ai_provider."
    "ollama_client.generate_response"
)
@patch(
    "app.services.ai_provider."
    "ai_client.generate_response"
)
def test_openai_success_does_not_use_ollama(
    mock_openai,
    mock_ollama,
):

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    mock_openai.return_value = (
        "OpenAI response"
    )

    response = (
        ai_provider_service
        .generate_response(
            messages=messages
        )
    )

    assert response == (
        "OpenAI response"
    )

    mock_openai.assert_called_once_with(
        messages=messages
    )

    mock_ollama.assert_not_called()


@patch(
    "app.services.ai_provider."
    "ollama_client.generate_response"
)
@patch(
    "app.services.ai_provider."
    "ai_client.generate_response"
)
def test_openai_failure_uses_ollama(
    mock_openai,
    mock_ollama,
):

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    mock_openai.side_effect = (
        RuntimeError(
            "OpenAI quota exceeded"
        )
    )

    mock_ollama.return_value = (
        "Ollama fallback response"
    )

    response = (
        ai_provider_service
        .generate_response(
            messages=messages
        )
    )

    assert response == (
        "Ollama fallback response"
    )

    mock_openai.assert_called_once_with(
        messages=messages
    )

    mock_ollama.assert_called_once_with(
        messages=messages
    )


@patch(
    "app.services.ai_provider."
    "settings.ai_fallback_enabled",
    False,
)
@patch(
    "app.services.ai_provider."
    "ollama_client.generate_response"
)
@patch(
    "app.services.ai_provider."
    "ai_client.generate_response"
)
def test_openai_failure_when_fallback_disabled(
    mock_openai,
    mock_ollama,
):

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    mock_openai.side_effect = (
        RuntimeError(
            "OpenAI unavailable"
        )
    )

    with pytest.raises(
        RuntimeError,
        match="OpenAI unavailable",
    ):

        ai_provider_service.generate_response(
            messages=messages
        )

    mock_openai.assert_called_once_with(
        messages=messages
    )

    mock_ollama.assert_not_called()