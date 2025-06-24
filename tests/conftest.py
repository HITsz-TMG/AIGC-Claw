"""
Shared pytest fixtures and configuration for the FilmAgent test suite.
"""
import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, MagicMock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_config():
    """Provide a mock configuration dictionary."""
    return {
        "topic": "Test Film Topic",
        "character_limit": 4,
        "scene_limit": 3,
        "stage1_verify_limit": 3,
        "stage2_verify_limit": 3,
        "stage3_verify_limit": 4,
        "model": "gpt-4",
        "api_key": "test-api-key"
    }


@pytest.fixture
def sample_character_profiles():
    """Provide sample character profiles for testing."""
    return [
        {
            "name": "Alice",
            "gender": "female",
            "age": 28,
            "personality": "outgoing and creative",
            "background": "artist and designer"
        },
        {
            "name": "Bob",
            "gender": "male", 
            "age": 32,
            "personality": "analytical and reserved",
            "background": "software engineer"
        }
    ]


@pytest.fixture
def sample_scene():
    """Provide a sample scene structure for testing."""
    return {
        "scene_information": {
            "who": ["Alice", "Bob"],
            "where": "Office",
            "what": "Discussing a new project"
        },
        "dialogues": [
            {
                "speaker": "Alice",
                "content": "I have an idea for our next project.",
                "actions": [
                    {
                        "character": "Alice",
                        "action": "Standing Talking",
                        "state": "standing"
                    }
                ]
            },
            {
                "speaker": "Bob",
                "content": "That sounds interesting, tell me more.",
                "actions": [
                    {
                        "character": "Bob",
                        "action": "Sitting Listening",
                        "state": "sitting"
                    }
                ]
            }
        ],
        "initial position": [
            {"character": "Alice", "position": "Position 1"},
            {"character": "Bob", "position": "Position 2"}
        ]
    }


@pytest.fixture
def sample_location_data():
    """Provide sample location position data."""
    return [
        {
            "id": "1",
            "description": "Near the window",
            "sittable": False,
            "fixed_angle": False
        },
        {
            "id": "2", 
            "description": "Office chair by desk",
            "sittable": True,
            "fixed_angle": False
        },
        {
            "id": "3",
            "description": "Corner sofa",
            "sittable": True,
            "fixed_angle": True
        }
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response generator."""
    def _mock_response(response_type="default"):
        responses = {
            "default": {"status": "success", "content": "Test response"},
            "character_profiles": [
                {"name": "TestChar1", "gender": "male", "age": 30},
                {"name": "TestChar2", "gender": "female", "age": 25}
            ],
            "scenes": [
                {
                    "sub-topic": "Introduction",
                    "selected-characters": ["TestChar1", "TestChar2"],
                    "selected-location": "Office",
                    "story-plot": "Characters meet for the first time",
                    "dialogue-goal": "Establish relationship"
                }
            ],
            "dialogues": [
                {
                    "speaker": "TestChar1",
                    "content": "Hello, nice to meet you.",
                    "actions": []
                }
            ]
        }
        return responses.get(response_type, responses["default"])
    return _mock_response


@pytest.fixture
def mock_file_system(temp_dir):
    """Set up a mock file system structure for testing."""
    # Create directory structure
    locations_dir = temp_dir / "Locations"
    locations_dir.mkdir()
    
    # Create sample location directories
    for location in ["Office", "Meeting room", "Reception Room"]:
        loc_dir = locations_dir / location
        loc_dir.mkdir()
        position_file = loc_dir / "position.json"
        position_file.write_text(json.dumps([
            {"id": "1", "description": f"Position 1 in {location}", "sittable": False, "fixed_angle": False},
            {"id": "2", "description": f"Position 2 in {location}", "sittable": True, "fixed_angle": False}
        ]))
    
    # Create actions and shots files
    actions_file = locations_dir / "actions.json"
    actions_file.write_text(json.dumps({
        "Standing Talking": "Character stands and talks",
        "Sitting Listening": "Character sits and listens",
        "Walking": "Character walks"
    }))
    
    shots_file = locations_dir / "shots.json"
    shots_file.write_text(json.dumps({
        "Close-up": "Close shot of character",
        "Long Shot": "Wide shot of scene",
        "Pan Shot": "Camera pans across scene"
    }))
    
    # Create Prompt directory
    prompt_dir = temp_dir / "Prompt"
    prompt_dir.mkdir()
    
    # Create Script directory
    script_dir = temp_dir / "Script"
    script_dir.mkdir()
    
    return temp_dir


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing LLM calls."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"test": "response"}'))]
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")
    

@pytest.fixture
def capture_logs(caplog):
    """Fixture to capture log messages during tests."""
    with caplog.at_level("DEBUG"):
        yield caplog


@pytest.fixture
def mock_external_apis(monkeypatch):
    """Mock all external API calls."""
    # Mock requests
    mock_requests = MagicMock()
    mock_requests.post.return_value.json.return_value = {"status": "success"}
    mock_requests.get.return_value.json.return_value = {"data": "test"}
    monkeypatch.setattr("requests.post", mock_requests.post)
    monkeypatch.setattr("requests.get", mock_requests.get)
    
    return mock_requests


@pytest.fixture
def reset_singleton():
    """Reset singleton instances between tests."""
    # This would be used to reset any singleton patterns in your code
    yield
    # Cleanup code here if needed


# Markers for different test types
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Test data fixtures
@pytest.fixture
def sample_prompt_template():
    """Sample prompt template for testing."""
    return """
    You are a {role} working on a film about {topic}.
    Please {action} based on the following information:
    {details}
    """


@pytest.fixture
def sample_tts_config():
    """Sample TTS configuration for testing."""
    return {
        "model_path": "/path/to/model",
        "speaker_embeddings": {
            "male": ["seed_11_restored_emb.pt"],
            "female": ["seed_492_restored_emb.pt"]
        },
        "sample_rate": 24000,
        "temperature": 0.3
    }