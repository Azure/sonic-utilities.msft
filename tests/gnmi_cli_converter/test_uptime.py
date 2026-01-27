"""
Uptime Command Tests
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


@pytest.fixture
def converter():
    """Fixture to create CLIConverter instance."""
    return CLIConverter()


class TestUptime:
    """Tests for show uptime command"""
    
    def test_basic_output(self, converter):
        """Test basic uptime output"""
        json_data = {"uptime": "up 3 weeks, 4 days, 10 hours, 15 minutes"}
        
        output = converter.convert(["uptime"], json_data)
        
        assert output == "up 3 weeks, 4 days, 10 hours, 15 minutes"
    
    def test_detailed_uptime(self, converter):
        """Test detailed uptime format"""
        json_data = {"uptime": "07:42:51 up 16 days, 14:51,  2 users,  load average: 0.00, 0.00, 0.00"}
        
        output = converter.convert(["uptime"], json_data)
        
        assert "07:42:51 up 16 days" in output
        assert "load average" in output
    
    def test_empty_uptime(self, converter):
        """Test empty uptime"""
        json_data = {"uptime": ""}
        
        output = converter.convert(["uptime"], json_data)
        
        assert output == ""
    
    def test_missing_key(self, converter):
        """Test missing uptime key"""
        json_data = {}
        
        output = converter.convert(["uptime"], json_data)
        
        assert output == ""
    
    def test_is_supported(self, converter):
        """Test uptime command is registered"""
        assert converter.is_supported(["uptime"]) is True
    
    def test_command_in_list(self, converter):
        """Test uptime appears in command list"""
        commands = converter.list_commands()
        command_paths = [cmd.path_elems for cmd in commands]
        
        assert ["uptime"] in command_paths
