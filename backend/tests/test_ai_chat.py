from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.schemas.ai_chat import AIChatRequest
from app.services.ai_response import (
    ai_response_service,
)


def test_ai_chat_request_trims_message():

    request = AIChatRequest(
        message="   Hello NeuroTwin   "
    )

    assert request.message == "Hello NeuroTwin"


def test_ai_chat_request_rejects_empty_message():

    with pytest.raises(
        ValidationError
    ):

        AIChatRequest(
            message="   "
        )


@patch(
    "app.services.ai_response."
    "ai_client.generate_response"
)
@patch(
    "app.services.ai_response."
    "ai_context_builder.build_context"
)
def test_ai_chat_response_service(
    mock_build_context,
    mock_generate_response,
):

    mock_build_context.return_value = [
        {
            "role": "system",
            "content": (
                "You are NeuroTwin."
            ),
        }
    ]

    mock_generate_response.return_value = (
        "Hello! I am your Digital Twin."
    )

    response = (
        ai_response_service.generate_response(
            db=None,
            digital_twin=None,
            conversation_id=(
                "test-conversation"
            ),
            user_id="test-user",
            user_message="Hello",
        )
    )

    assert response == (
        "Hello! I am your Digital Twin."
    )

    mock_build_context.assert_called_once_with(
        db=None,
        digital_twin=None,
        conversation_id=(
            "test-conversation"
        ),
        user_id="test-user",
    )

    mock_generate_response.assert_called_once()

    messages = (
        mock_generate_response
        .call_args
        .kwargs["messages"]
    )

    assert messages[-1] == {
        "role": "user",
        "content": "Hello",
    }