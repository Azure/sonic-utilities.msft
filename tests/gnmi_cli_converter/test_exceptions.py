"""
Exception Classes Tests
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


class TestExceptions:
    """Exception classes tests"""
    
    def test_path_not_found_error(self):
        """Test PathNotFoundError"""
        from gnmi_cli_converter.exceptions import PathNotFoundError
        
        error = PathNotFoundError(["test", "path"])
        assert error.path_elems == ["test", "path"]
        assert "test" in str(error)
        assert "path" in str(error)
    
    def test_exception_hierarchy(self):
        """Test exception inheritance hierarchy"""
        from gnmi_cli_converter.exceptions import (
            CLIConverterError,
            PathNotFoundError,
            InvalidJSONError,
            RenderError,
            MissingFieldError
        )
        
        assert issubclass(PathNotFoundError, CLIConverterError)
        assert issubclass(InvalidJSONError, CLIConverterError)
        assert issubclass(RenderError, CLIConverterError)
        assert issubclass(MissingFieldError, CLIConverterError)
