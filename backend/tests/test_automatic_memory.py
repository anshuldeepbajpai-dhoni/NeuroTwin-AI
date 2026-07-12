from types import SimpleNamespace
from unittest.mock import MagicMock
from unittest.mock import patch

from app.models.memory import Memory
from app.services.automatic_memory import (
    automatic_memory_service,
)


def create_mock_user():
    """
    Create a simple test user.
    """

    return SimpleNamespace(
        id="test-user-id"
    )


def create_mock_memory(
    title: str,
    content: str,
    category: str = "goal",
):
    """
    Create a mocked Memory object.
    """

    memory = MagicMock(
        spec=Memory
    )

    memory.id = "test-memory-id"
    memory.user_id = "test-user-id"
    memory.title = title
    memory.content = content
    memory.category = category
    memory.importance = 8
    memory.is_favorite = False

    return memory


def test_normalize_memory_text():
    """
    Test memory text normalization.
    """

    result = (
        automatic_memory_service
        .normalize_text(
            "  AI    Engineering   Goal  "
        )
    )

    assert result == (
        "ai engineering goal"
    )


def test_find_exact_matching_memory():
    """
    Test exact memory matching.
    """

    db = MagicMock()

    existing_memory = (
        create_mock_memory(
            title="AI Engineering Goal",
            content=(
                "The user wants to become "
                "an AI engineer."
            ),
        )
    )

    (
        db.query.return_value
        .filter.return_value
        .all.return_value
    ) = [
        existing_memory
    ]

    memory, similarity = (
        automatic_memory_service
        .find_matching_memory(
            db=db,
            user_id="test-user-id",
            title="AI Engineering Goal",
            content=(
                "The user wants to become "
                "an AI engineer."
            ),
            category="goal",
        )
    )

    assert memory is existing_memory
    assert similarity == 1.0


def test_find_no_matching_memory():
    """
    Test behavior when no saved memory
    matches the extracted information.
    """

    db = MagicMock()

    (
        db.query.return_value
        .filter.return_value
        .all.return_value
    ) = []

    memory, similarity = (
        automatic_memory_service
        .find_matching_memory(
            db=db,
            user_id="test-user-id",
            title="AI Engineering Goal",
            content=(
                "The user wants to become "
                "an AI engineer."
            ),
            category="goal",
        )
    )

    assert memory is None
    assert similarity == 0.0


@patch(
    "app.services.automatic_memory."
    "create_memory"
)
@patch(
    "app.services.automatic_memory."
    "memory_extractor.extract"
)
@patch.object(
    automatic_memory_service,
    "find_matching_memory",
)
def test_new_memory_is_created(
    mock_find_matching_memory,
    mock_extract,
    mock_create_memory,
):
    """
    Test creation of a new memory when
    no related saved memory exists.
    """

    db = MagicMock()

    current_user = (
        create_mock_user()
    )

    extracted_memory = {
        "should_save": True,
        "title": "AI Engineering Goal",
        "content": (
            "The user wants to become "
            "an AI engineer."
        ),
        "category": "goal",
        "importance": 5,
    }

    mock_extract.return_value = (
        extracted_memory
    )

    mock_find_matching_memory.return_value = (
        None,
        0.0,
    )

    saved_memory = MagicMock(
        spec=Memory
    )

    mock_create_memory.return_value = (
        saved_memory
    )

    result = (
        automatic_memory_service
        .process_message(
            db=db,
            current_user=current_user,
            user_message=(
                "I want to become "
                "an AI engineer."
            ),
        )
    )

    assert result is saved_memory

    mock_extract.assert_called_once_with(
        "I want to become "
        "an AI engineer."
    )

    mock_find_matching_memory.assert_called_once_with(
        db=db,
        user_id="test-user-id",
        title="AI Engineering Goal",
        content=(
            "The user wants to become "
            "an AI engineer."
        ),
        category="goal",
    )

    mock_create_memory.assert_called_once()

    call_arguments = (
        mock_create_memory.call_args.kwargs
    )

    assert call_arguments["db"] is db

    assert (
        call_arguments["current_user"]
        is current_user
    )

    memory_data = (
        call_arguments["memory_data"]
    )

    assert (
        memory_data.title
        == "AI Engineering Goal"
    )

    assert memory_data.content == (
        "The user wants to become "
        "an AI engineer."
    )

    assert (
        memory_data.category
        == "goal"
    )

    assert (
        memory_data.importance
        == 5
    )

    assert (
        memory_data.is_favorite
        is False
    )


@patch(
    "app.services.automatic_memory."
    "create_memory"
)
@patch(
    "app.services.automatic_memory."
    "memory_extractor.extract"
)
@patch.object(
    automatic_memory_service,
    "find_matching_memory",
)
def test_duplicate_memory_is_skipped(
    mock_find_matching_memory,
    mock_extract,
    mock_create_memory,
):
    """
    Test that highly similar memories
    are not created again.
    """

    db = MagicMock()

    current_user = (
        create_mock_user()
    )

    existing_memory = (
        create_mock_memory(
            title="AI Engineering Goal",
            content=(
                "The user wants to become "
                "an AI engineer."
            ),
        )
    )

    mock_extract.return_value = {
        "should_save": True,
        "title": "AI Engineering Goal",
        "content": (
            "The user wants to become "
            "an AI engineer."
        ),
        "category": "goal",
        "importance": 5,
    }

    mock_find_matching_memory.return_value = (
        existing_memory,
        1.0,
    )

    result = (
        automatic_memory_service
        .process_message(
            db=db,
            current_user=current_user,
            user_message=(
                "I want to become "
                "an AI engineer."
            ),
        )
    )

    assert result is existing_memory

    mock_create_memory.assert_not_called()


@patch(
    "app.services.automatic_memory."
    "create_memory"
)
@patch.object(
    automatic_memory_service,
    "update_memory",
)
@patch(
    "app.services.automatic_memory."
    "memory_extractor.extract"
)
@patch.object(
    automatic_memory_service,
    "find_matching_memory",
)
def test_related_memory_is_updated(
    mock_find_matching_memory,
    mock_extract,
    mock_update_memory,
    mock_create_memory,
):
    """
    Test that related newer information
    updates an existing memory.
    """

    db = MagicMock()

    current_user = (
        create_mock_user()
    )

    existing_memory = (
        create_mock_memory(
            title="Learning Flask",
            content=(
                "The user is learning Flask."
            ),
            category="skill",
        )
    )

    extracted_memory = {
        "should_save": True,
        "title": "Learning FastAPI",
        "content": (
            "The user is now learning "
            "FastAPI instead of Flask."
        ),
        "category": "skill",
        "importance": 5,
    }

    mock_extract.return_value = (
        extracted_memory
    )

    mock_find_matching_memory.return_value = (
        existing_memory,
        0.70,
    )

    updated_memory = MagicMock(
        spec=Memory
    )

    mock_update_memory.return_value = (
        updated_memory
    )

    result = (
        automatic_memory_service
        .process_message(
            db=db,
            current_user=current_user,
            user_message=(
                "I am now learning FastAPI "
                "instead of Flask."
            ),
        )
    )

    assert result is updated_memory

    mock_update_memory.assert_called_once_with(
        db=db,
        memory=existing_memory,
        extracted_memory=(
            extracted_memory
        ),
    )

    mock_create_memory.assert_not_called()


@patch(
    "app.services.automatic_memory."
    "create_memory"
)
@patch(
    "app.services.automatic_memory."
    "memory_extractor.extract"
)
def test_non_memory_message_is_ignored(
    mock_extract,
    mock_create_memory,
):
    """
    Test that temporary messages are
    not stored as memories.
    """

    db = MagicMock()

    current_user = (
        create_mock_user()
    )

    mock_extract.return_value = {
        "should_save": False,
        "title": None,
        "content": None,
        "category": None,
        "importance": None,
    }

    result = (
        automatic_memory_service
        .process_message(
            db=db,
            current_user=current_user,
            user_message=(
                "Hello, how are you?"
            ),
        )
    )

    assert result is None

    db.query.assert_not_called()

    mock_create_memory.assert_not_called()


def test_existing_memory_is_updated():
    """
    Test direct database update behavior.
    """

    db = MagicMock()

    existing_memory = (
        create_mock_memory(
            title="Learning Flask",
            content=(
                "The user is learning Flask."
            ),
            category="skill",
        )
    )

    extracted_memory = {
        "should_save": True,
        "title": "Learning FastAPI",
        "content": (
            "The user is now learning "
            "FastAPI instead of Flask."
        ),
        "category": "skill",
        "importance": 5,
    }

    result = (
        automatic_memory_service
        .update_memory(
            db=db,
            memory=existing_memory,
            extracted_memory=(
                extracted_memory
            ),
        )
    )

    assert result is existing_memory

    assert (
        existing_memory.title
        == "Learning FastAPI"
    )

    assert existing_memory.content == (
        "The user is now learning "
        "FastAPI instead of Flask."
    )

    assert (
        existing_memory.category
        == "skill"
    )

    assert (
        existing_memory.importance
        == 5
    )

    db.commit.assert_called_once()

    db.refresh.assert_called_once_with(
        existing_memory
    )