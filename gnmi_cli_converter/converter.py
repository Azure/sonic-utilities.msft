"""
CLI Converter Main Class

Provides interface for converting GNMI JSON to CLI format.
"""

from typing import List, Any
from dataclasses import dataclass
from .registry import get_renderer, list_commands as registry_list_commands, is_supported as registry_is_supported
from .exceptions import PathNotFoundError, RenderError

# Logger instance
from sonic_py_common.logger import Logger

SYSLOG_IDENTIFIER = "gnmi_cli_converter"
log = Logger(SYSLOG_IDENTIFIER)


@dataclass
class CommandInfo:
    """Command information (for callers to query supported command list)"""
    path_elems: List[str]  # ["buffer_pool", "watermark"] or ["interfaces", "errors", "*"]
    command: str           # "show buffer_pool watermark"


class CLIConverter:
    """
    Converter for GNMI JSON to CLI format.
    
    Example:
        >>> converter = CLIConverter()
        >>> json_data = {"egress_lossless_pool": {"Bytes": "12345"}}
        >>> output = converter.convert(["buffer_pool", "watermark"], json_data)
        >>> print(output)
        Shared pool maximum occupancy:
                        Pool  Bytes
        ---------------------  -----
         egress_lossless_pool  12345
    """
    
    def convert(self, path_elems: List[str], json_data: Any) -> str:
        """
        Convert GNMI JSON to CLI format text.
        
        Args:
            path_elems: Path element array containing the full path (with parameter values)
                       - Without parameters: ["buffer_pool", "watermark"]
                       - With parameters: ["interfaces", "errors", "Ethernet0"]
                       (without "SHOW" prefix)
            json_data: JSON data returned by GNMI (already parsed to Python object)
        
        Returns:
            CLI format text output
        
        Raises:
            PathNotFoundError: Path not registered
            RenderError: Rendering failed
        """
        try:
            # 1. Find render function
            log.log_debug(f"Looking up renderer for path: {path_elems}")
            render_func = get_renderer(path_elems)
            
            # 2. Call render function
            log.log_debug(f"Rendering JSON data for path: {path_elems}")
            output = render_func(json_data, path_elems)
            
            log.log_debug(f"Successfully rendered path: {path_elems}")
            return output
        
        except PathNotFoundError:
            log.log_warning(f"Path not found: {path_elems}")
            raise
        
        except Exception as e:
            log.log_error(f"Failed to render path {path_elems}: {e}")
            raise RenderError(f"Failed to render path {path_elems}: {e}") from e
    
    def is_supported(self, path_elems: List[str]) -> bool:
        """
        Check if the path is supported.
        
        Args:
            path_elems: Path element array
        
        Returns:
            True if supported, False otherwise
        """
        return registry_is_supported(path_elems)
    
    def list_commands(self) -> List[CommandInfo]:
        """
        Get list of all supported commands.
        
        Returns:
            List of command information
        """
        entries = registry_list_commands()
        return [
            CommandInfo(
                path_elems=entry.path_pattern,
                command=entry.command
            )
            for entry in entries
        ]
