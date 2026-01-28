"""
CLIConverter Core Functionality Tests
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

from gnmi_cli_converter import CLIConverter, PathNotFoundError, RenderError


@pytest.fixture
def converter():
    """Fixture to create CLIConverter instance."""
    return CLIConverter()


@pytest.fixture
def buffer_pool_watermark_json():
    """Test JSON data for buffer_pool watermark command."""
    return {
        "egress_lossless_pool": {"Bytes": "12345"},
        "egress_lossy_pool": {"Bytes": "67890"},
        "ingress_lossless_pool": {"Bytes": "24680"}
    }


class TestCLIConverter:
    """Tests for CLIConverter class"""
    
    def test_convert_basic(self, converter, buffer_pool_watermark_json):
        """Test basic convert functionality"""
        output = converter.convert(
            buffer_pool_watermark_json,
            path_elems=["buffer_pool", "watermark"]
        )
        
        # Check output contains title
        assert "Shared pool maximum occupancy:" in output
        
        # Check output contains all pool names
        assert "egress_lossless_pool" in output
        assert "egress_lossy_pool" in output
        assert "ingress_lossless_pool" in output
        
        # Check output contains all values
        assert "12345" in output
        assert "67890" in output
        assert "24680" in output
    
    def test_convert_with_xpath(self, converter, buffer_pool_watermark_json):
        """Test convert using xpath"""
        output = converter.convert(
            buffer_pool_watermark_json,
            xpath="/buffer_pool/watermark"
        )
        
        assert "Shared pool maximum occupancy:" in output
        assert "egress_lossless_pool" in output
    
    def test_convert_with_xpath_no_leading_slash(self, converter, buffer_pool_watermark_json):
        """Test convert using xpath without leading slash"""
        output = converter.convert(
            buffer_pool_watermark_json,
            xpath="buffer_pool/watermark"
        )
        
        assert "Shared pool maximum occupancy:" in output
    
    def test_convert_with_command(self, converter, buffer_pool_watermark_json):
        """Test convert using show command"""
        output = converter.convert(
            buffer_pool_watermark_json,
            command="show buffer_pool watermark"
        )
        
        assert "Shared pool maximum occupancy:" in output
        assert "egress_lossless_pool" in output
    
    def test_convert_with_command_no_show_prefix(self, converter, buffer_pool_watermark_json):
        """Test convert using command without show prefix"""
        output = converter.convert(
            buffer_pool_watermark_json,
            command="buffer_pool watermark"
        )
        
        assert "Shared pool maximum occupancy:" in output
    
    def test_convert_multiple_specifiers_error(self, converter, buffer_pool_watermark_json):
        """Test error when multiple path specifiers provided"""
        with pytest.raises(ValueError) as exc_info:
            converter.convert(
                buffer_pool_watermark_json,
                path_elems=["buffer_pool", "watermark"],
                xpath="/buffer_pool/watermark"
            )
        
        assert "exactly one" in str(exc_info.value)
    
    def test_convert_no_specifier_error(self, converter, buffer_pool_watermark_json):
        """Test error when no path specifier provided"""
        with pytest.raises(ValueError) as exc_info:
            converter.convert(buffer_pool_watermark_json)
        
        assert "exactly one" in str(exc_info.value)
    
    def test_is_supported_with_xpath(self, converter):
        """Test is_supported with xpath"""
        assert converter.is_supported(xpath="/buffer_pool/watermark") is True
        assert converter.is_supported(xpath="/unknown/path") is False
    
    def test_is_supported_with_command(self, converter):
        """Test is_supported with command"""
        assert converter.is_supported(command="show buffer_pool watermark") is True
        assert converter.is_supported(command="show unknown path") is False
    
    def test_xpath_to_path_elems_basic(self, converter):
        """Test _xpath_to_path_elems basic parsing"""
        path_elems, options = CLIConverter._xpath_to_path_elems("/buffer_pool/watermark")
        assert path_elems == ["buffer_pool", "watermark"]
        assert options == {}
    
    def test_xpath_to_path_elems_with_options(self, converter):
        """Test _xpath_to_path_elems with options"""
        path_elems, options = CLIConverter._xpath_to_path_elems(
            "/interfaces/counters[printall=true][interfaces=Ethernet0]"
        )
        assert path_elems == ["interfaces", "counters"]
        assert options == {"printall": True, "interfaces": "Ethernet0"}
    
    def test_xpath_to_path_elems_type_conversion(self, converter):
        """Test _xpath_to_path_elems converts types correctly"""
        path_elems, options = CLIConverter._xpath_to_path_elems(
            "/queue/counters[nonzero=true][period=10][verbose=false]"
        )
        assert options["nonzero"] is True
        assert options["period"] == 10
        assert options["verbose"] is False
    
    def test_command_to_path_elems_basic(self, converter):
        """Test _command_to_path_elems basic parsing"""
        path_elems, options = CLIConverter._command_to_path_elems("show buffer_pool watermark")
        assert path_elems == ["buffer_pool", "watermark"]
        assert options == {}
    
    def test_command_to_path_elems_with_options(self, converter):
        """Test _command_to_path_elems with options"""
        path_elems, options = CLIConverter._command_to_path_elems(
            "show interfaces counters --printall --interfaces=Ethernet0"
        )
        assert path_elems == ["interfaces", "counters"]
        assert options == {"printall": True, "interfaces": "Ethernet0"}
    
    def test_command_to_path_elems_type_conversion(self, converter):
        """Test _command_to_path_elems converts types correctly"""
        path_elems, options = CLIConverter._command_to_path_elems(
            "show queue counters --nonzero --period=10 --verbose=false"
        )
        assert options["nonzero"] is True
        assert options["period"] == 10
        assert options["verbose"] is False
    
    def test_convert_xpath_with_options(self, converter, buffer_pool_watermark_json):
        """Test convert using xpath with embedded options"""
        # Note: buffer_pool doesn't use options, but we verify options are parsed
        output = converter.convert(
            buffer_pool_watermark_json,
            xpath="/buffer_pool/watermark[verbose=true]"
        )
        assert "Shared pool maximum occupancy:" in output
    
    def test_convert_command_with_options(self, converter, buffer_pool_watermark_json):
        """Test convert using command with embedded options"""
        output = converter.convert(
            buffer_pool_watermark_json,
            command="show buffer_pool watermark --verbose"
        )
        assert "Shared pool maximum occupancy:" in output

    def test_convert_not_found(self, converter):
        """Test unregistered path throws PathNotFoundError"""
        with pytest.raises(PathNotFoundError) as exc_info:
            converter.convert({}, path_elems=["unknown", "path"])
        
        assert "unknown" in str(exc_info.value)
    
    def test_is_supported_registered(self, converter):
        """Test registered path returns True"""
        assert converter.is_supported(path_elems=["buffer_pool", "watermark"]) is True
        assert converter.is_supported(path_elems=["buffer_pool", "persistent-watermark"]) is True
    
    def test_is_supported_not_registered(self, converter):
        """Test unregistered path returns False"""
        assert converter.is_supported(path_elems=["unknown", "path"]) is False
        assert converter.is_supported(path_elems=[]) is False
    
    def test_list_commands(self, converter):
        """Test listing all supported commands"""
        commands = converter.list_commands()
        
        # Check returns a list
        assert isinstance(commands, list)
        
        # Check contains at least buffer_pool commands
        command_strs = [cmd.command for cmd in commands]
        assert any("buffer_pool" in cmd for cmd in command_strs)
        
        # Check each command has path_elems and command attributes
        for cmd in commands:
            assert hasattr(cmd, 'path_elems')
            assert hasattr(cmd, 'command')
            assert isinstance(cmd.path_elems, list)
            assert isinstance(cmd.command, str)


class TestRegistry:
    """Registry functionality tests"""
    
    def test_register_decorator(self):
        """Test @register decorator works correctly"""
        from gnmi_cli_converter.registry import _REGISTRY
        
        # Check buffer_pool/watermark is registered
        assert "buffer_pool/watermark" in _REGISTRY
        assert "buffer_pool/persistent-watermark" in _REGISTRY
    
    def test_wildcard_matching(self):
        """Test wildcard matching functionality"""
        from gnmi_cli_converter.registry import register, get_renderer, clear_registry, _REGISTRY
        
        # Save original registry
        original_registry = _REGISTRY.copy()
        
        try:
            # Register a command with wildcard
            @register(["test", "wildcard", "*"])
            def render_test_wildcard(json_data, path_elems, options):
                return f"param: {path_elems[2]}"
            
            # Test wildcard matching
            renderer = get_renderer(["test", "wildcard", "Ethernet0"])
            assert renderer({"data": "test"}, ["test", "wildcard", "Ethernet0"], {}) == "param: Ethernet0"
            
            renderer = get_renderer(["test", "wildcard", "Ethernet4"])
            assert renderer({"data": "test"}, ["test", "wildcard", "Ethernet4"], {}) == "param: Ethernet4"
        
        finally:
            # Restore original registry
            _REGISTRY.clear()
            _REGISTRY.update(original_registry)
