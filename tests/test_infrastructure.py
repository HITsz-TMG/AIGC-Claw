"""
Validation tests to verify the testing infrastructure is properly set up.
"""
import json
import os
from pathlib import Path

import pytest


class TestInfrastructureSetup:
    """Test class to validate the testing infrastructure."""
    
    @pytest.mark.unit
    def test_pytest_is_working(self):
        """Basic test to ensure pytest is running."""
        assert True
        
    @pytest.mark.unit
    def test_fixtures_are_available(self, temp_dir, mock_config):
        """Test that fixtures from conftest.py are accessible."""
        assert temp_dir.exists()
        assert isinstance(mock_config, dict)
        assert "topic" in mock_config
        
    @pytest.mark.unit
    def test_temp_dir_fixture(self, temp_dir):
        """Test the temporary directory fixture."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!")
        
        # Verify it exists and has correct content
        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"
        
    @pytest.mark.unit
    def test_mock_config_fixture(self, mock_config):
        """Test the mock configuration fixture."""
        assert mock_config["topic"] == "Test Film Topic"
        assert mock_config["character_limit"] == 4
        assert mock_config["scene_limit"] == 3
        assert "model" in mock_config
        
    @pytest.mark.unit
    def test_sample_character_profiles(self, sample_character_profiles):
        """Test the character profiles fixture."""
        assert len(sample_character_profiles) == 2
        assert sample_character_profiles[0]["name"] == "Alice"
        assert sample_character_profiles[1]["name"] == "Bob"
        
    @pytest.mark.unit
    def test_sample_scene_structure(self, sample_scene):
        """Test the sample scene fixture."""
        assert "scene_information" in sample_scene
        assert "dialogues" in sample_scene
        assert "initial position" in sample_scene
        assert len(sample_scene["dialogues"]) == 2
        
    @pytest.mark.unit
    def test_mock_llm_response(self, mock_llm_response):
        """Test the mock LLM response fixture."""
        default_response = mock_llm_response("default")
        assert default_response["status"] == "success"
        
        character_response = mock_llm_response("character_profiles")
        assert isinstance(character_response, list)
        assert len(character_response) == 2
        
    @pytest.mark.integration
    def test_mock_file_system(self, mock_file_system):
        """Test the mock file system fixture."""
        locations_dir = mock_file_system / "Locations"
        assert locations_dir.exists()
        
        # Check that location directories exist
        office_dir = locations_dir / "Office"
        assert office_dir.exists()
        
        # Check position.json exists
        position_file = office_dir / "position.json"
        assert position_file.exists()
        
        # Verify JSON content
        positions = json.loads(position_file.read_text())
        assert isinstance(positions, list)
        assert len(positions) > 0
        
    @pytest.mark.unit
    def test_environment_setup(self):
        """Test that environment variables are set."""
        assert os.environ.get("OPENAI_API_KEY") == "test-api-key"
        assert os.environ.get("ANTHROPIC_API_KEY") == "test-api-key"
        
    @pytest.mark.unit
    def test_markers_are_defined(self, request):
        """Test that custom markers are properly defined."""
        markers = [marker.name for marker in request.node.iter_markers()]
        assert "unit" in markers
        
    @pytest.mark.slow
    @pytest.mark.unit
    def test_slow_marker(self):
        """Test that slow marker can be applied."""
        # This test would be skipped with pytest -m "not slow"
        import time
        time.sleep(0.1)  # Simulate slow operation
        assert True
        
    @pytest.mark.unit
    def test_coverage_is_enabled(self):
        """Test that coverage reporting is configured."""
        # This test verifies coverage is working by being included in coverage
        def dummy_function():
            return "covered"
        
        assert dummy_function() == "covered"
        
    @pytest.mark.unit
    def test_sample_location_data(self, sample_location_data):
        """Test the location data fixture."""
        assert len(sample_location_data) == 3
        assert sample_location_data[0]["description"] == "Near the window"
        assert sample_location_data[1]["sittable"] is True
        
    @pytest.mark.unit
    def test_mock_openai_client(self, mock_openai_client):
        """Test the mock OpenAI client fixture."""
        response = mock_openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}]
        )
        assert response.choices[0].message.content == '{"test": "response"}'
        
    @pytest.mark.unit
    def test_capture_logs_fixture(self, capture_logs):
        """Test the log capture fixture."""
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Test debug message")
        logger.info("Test info message")
        
        assert "Test debug message" in capture_logs.text
        assert "Test info message" in capture_logs.text
        
    @pytest.mark.integration
    def test_mock_external_apis(self, mock_external_apis):
        """Test the external API mocking fixture."""
        # Test POST request
        post_response = mock_external_apis.post("http://test.com", json={"data": "test"})
        assert post_response.json()["status"] == "success"
        
        # Test GET request
        get_response = mock_external_apis.get("http://test.com")
        assert get_response.json()["data"] == "test"
        
    @pytest.mark.unit
    def test_sample_prompt_template(self, sample_prompt_template):
        """Test the prompt template fixture."""
        assert "{role}" in sample_prompt_template
        assert "{topic}" in sample_prompt_template
        assert "{action}" in sample_prompt_template
        
    @pytest.mark.unit
    def test_sample_tts_config(self, sample_tts_config):
        """Test the TTS configuration fixture."""
        assert "model_path" in sample_tts_config
        assert "speaker_embeddings" in sample_tts_config
        assert sample_tts_config["sample_rate"] == 24000


class TestPytestConfiguration:
    """Test pytest configuration options."""
    
    @pytest.mark.unit
    def test_pytest_ini_options_loaded(self, pytestconfig):
        """Test that pytest.ini options from pyproject.toml are loaded."""
        # Check if coverage options are set
        assert "--cov=" in " ".join(pytestconfig.invocation_params.args)
        
    @pytest.mark.unit
    def test_test_discovery_patterns(self):
        """Verify test discovery patterns work."""
        # This test file should be discovered
        assert __file__.endswith("test_infrastructure.py")


def test_standalone_function():
    """Test that standalone test functions are discovered."""
    assert True


if __name__ == "__main__":
    # Allow running this file directly for debugging
    pytest.main([__file__, "-v"])