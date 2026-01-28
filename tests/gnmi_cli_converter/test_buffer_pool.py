"""
Buffer Pool Command Tests
"""

import pytest
import sys
import os
from unittest.mock import MagicMock

# Add gnmi_cli_converter to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Add current test directory to sys.path for common import
sys.path.insert(0, os.path.dirname(__file__))

# Mock sonic_py_common.logger before importing gnmi_cli_converter
mock_logger = MagicMock()
sys.modules['sonic_py_common'] = MagicMock()
sys.modules['sonic_py_common.logger'] = MagicMock()
sys.modules['sonic_py_common.logger'].Logger = MagicMock(return_value=mock_logger)

from gnmi_cli_converter import CLIConverter
from common import load_json, load_expected


@pytest.fixture
def converter():
    """Fixture to create CLIConverter instance."""
    return CLIConverter()


@pytest.fixture
def buffer_pool_watermark_json():
    """Test JSON data for buffer_pool watermark command."""
    return load_json("buffer_pool_watermark.json")


@pytest.fixture
def buffer_pool_persistent_watermark_json():
    """Test JSON data for buffer_pool persistent-watermark command."""
    return load_json("buffer_pool_persistent_watermark.json")


class TestBufferPoolWatermark:
    """Tests for show buffer_pool watermark command"""
    
    def test_output_matches_expected(self, converter, buffer_pool_watermark_json):
        """Test output matches expected file exactly"""
        output = converter.convert(
            buffer_pool_watermark_json,
            path_elems=["buffer_pool", "watermark"]
        )
        expected = load_expected("buffer_pool_watermark.txt")
        assert output == expected
    
    def test_natural_sorting(self, converter):
        """Test natural sorting"""
        json_data = {
            "pool10": {"Bytes": "100"},
            "pool2": {"Bytes": "200"},
            "pool1": {"Bytes": "300"}
        }
        
        output = converter.convert(
            json_data,
            path_elems=["buffer_pool", "watermark"]
        )
        
        # Check all pools are in output
        assert "pool1" in output
        assert "pool2" in output
        assert "pool10" in output
        
        # Check natural sorting (pool1, pool2, pool10)
        pos1 = output.find("pool1")
        pos2 = output.find("pool2")
        pos10 = output.find("pool10")
        
        # pool1 should be before pool2 (ignoring pool10)
        assert pos1 < pos2
        # pool2 should be before pool10
        assert pos2 < pos10
    
    def test_empty_data(self, converter):
        """Test empty data handling"""
        output = converter.convert(
            {},
            path_elems=["buffer_pool", "watermark"]
        )
        
        assert "Shared pool maximum occupancy:" in output
        assert "No data available" in output
    
    def test_missing_bytes_field(self, converter):
        """Test handling of missing Bytes field"""
        json_data = {
            "pool_without_bytes": {"other_field": "value"}
        }
        
        output = converter.convert(
            json_data,
            path_elems=["buffer_pool", "watermark"]
        )
        
        assert "pool_without_bytes" in output
        assert "N/A" in output


class TestBufferPoolPersistentWatermark:
    """Tests for show buffer_pool persistent-watermark command"""
    
    def test_output_matches_expected(self, converter, buffer_pool_persistent_watermark_json):
        """Test output matches expected file exactly"""
        output = converter.convert(
            buffer_pool_persistent_watermark_json,
            path_elems=["buffer_pool", "persistent-watermark"]
        )
        expected = load_expected("buffer_pool_persistent_watermark.txt")
        assert output == expected
    
    def test_empty_data(self, converter):
        """Test empty data handling"""
        output = converter.convert(
            {},
            path_elems=["buffer_pool", "persistent-watermark"]
        )
        
        assert "Shared pool maximum occupancy:" in output
        assert "No data available" in output


class TestBufferPoolIntegration:
    """Buffer Pool command integration tests"""
    
    def test_both_commands_registered(self, converter):
        """Test both commands are registered"""
        assert converter.is_supported(path_elems=["buffer_pool", "watermark"]) is True
        assert converter.is_supported(path_elems=["buffer_pool", "persistent-watermark"]) is True
    
    def test_commands_in_list(self, converter):
        """Test commands appear in list"""
        commands = converter.list_commands()
        command_paths = [cmd.path_elems for cmd in commands]
        
        assert ["buffer_pool", "watermark"] in command_paths
        assert ["buffer_pool", "persistent-watermark"] in command_paths
    
    def test_command_descriptions(self, converter):
        """Test command descriptions are correct"""
        commands = converter.list_commands()
        
        watermark_cmd = next(
            (cmd for cmd in commands if cmd.path_elems == ["buffer_pool", "watermark"]),
            None
        )
        assert watermark_cmd is not None
        assert "show buffer_pool watermark" in watermark_cmd.command
