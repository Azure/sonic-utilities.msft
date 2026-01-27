"""
Utils Module Tests
"""

import pytest
import sys
import os
from unittest.mock import MagicMock

# Add gnmi_cli_converter to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock sonic_py_common.logger before importing gnmi_cli_converter
mock_logger = MagicMock()
sys.modules['sonic_py_common'] = MagicMock()
sys.modules['sonic_py_common.logger'] = MagicMock()
sys.modules['sonic_py_common.logger'].Logger = MagicMock(return_value=mock_logger)


class TestUtils:
    """Utils functions tests"""
    
    def test_passthrough(self):
        """Test passthrough function"""
        from gnmi_cli_converter.utils import passthrough
        
        json_data = {"output": "Hello, World!"}
        assert passthrough(json_data) == "Hello, World!"
        
        json_data = {"output": ""}
        assert passthrough(json_data) == ""
        
        json_data = {}
        assert passthrough(json_data) == ""
    
    def test_passthrough_custom_key(self):
        """Test passthrough function with custom key"""
        from gnmi_cli_converter.utils import passthrough
        
        json_data = {"result": "Custom value"}
        assert passthrough(json_data, key="result") == "Custom value"
    
    def test_tabulate_dict(self):
        """Test tabulate_dict function"""
        from gnmi_cli_converter.utils import tabulate_dict
        
        rows = [("pool1", "100"), ("pool2", "200")]
        headers = ["Pool", "Bytes"]
        
        output = tabulate_dict(rows, headers)
        
        assert "Pool" in output
        assert "Bytes" in output
        assert "pool1" in output
        assert "100" in output
    
    def test_tabulate_dict_with_title(self):
        """Test tabulate_dict function with title"""
        from gnmi_cli_converter.utils import tabulate_dict
        
        rows = [("pool1", "100")]
        headers = ["Pool", "Bytes"]
        
        output = tabulate_dict(rows, headers, title="My Title:")
        
        assert "My Title:" in output
        assert output.startswith("My Title:")
    
    def test_key_value_pairs(self):
        """Test key_value_pairs function"""
        from gnmi_cli_converter.utils import key_value_pairs
        
        json_data = {"mmu_size": "12345678", "cell_size": "256"}
        mapping = {"mmu_size": "MMU Size", "cell_size": "Cell Size"}
        
        output = key_value_pairs(json_data, mapping)
        
        assert "MMU Size: 12345678" in output
        assert "Cell Size: 256" in output
