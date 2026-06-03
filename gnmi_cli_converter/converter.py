"""
CLI Converter Main Class

Provides interface for converting GNMI JSON to CLI format.
"""

from typing import List, Any, Dict, Optional, Union, Tuple
from dataclasses import dataclass
import re
from .registry import get_renderer, list_commands as registry_list_commands, is_supported as registry_is_supported
from .exceptions import PathNotFoundError, RenderError

# Logger instance
from sonic_py_common.logger import Logger

SYSLOG_IDENTIFIER = "gnmi_cli_converter"
log = Logger(SYSLOG_IDENTIFIER)


@dataclass
class CommandInfo:
    """Command information (for callers to query supported command list)"""
    path_elems: List[str]  # Pattern with wildcards: ["interfaces", "errors", "*"]
    command: str           # "show interfaces errors <interface_name>"


class CLIConverter:
    """
    Converter for GNMI JSON to CLI format.
    
    Example:
        >>> converter = CLIConverter()
        >>> json_data = {"egress_lossless_pool": {"Bytes": "12345"}}
        >>> # Three equivalent ways to call convert:
        >>> output = converter.convert(json_data, path_elems=["buffer_pool", "watermark"])
        >>> output = converter.convert(json_data, xpath="/buffer_pool/watermark")
        >>> output = converter.convert(json_data, command="show buffer_pool watermark")
        >>> print(output)
        Shared pool maximum occupancy:
                        Pool  Bytes
        ---------------------  -----
         egress_lossless_pool  12345
    """
    
    @staticmethod
    def _xpath_to_path_elems(xpath: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        Convert xpath string to path_elems list and options dict.
        
        Args:
            xpath: XPath string, e.g."/interfaces/counters[printall=true][period=5]"
        
        Returns:
            Tuple of (path_elems, options)
            - path_elems: e.g. ["interfaces", "counters"]
            - options: e.g. {"printall": True, "period": 5}
        
        Examples:
            >>> CLIConverter._xpath_to_path_elems("/buffer_pool/watermark")
            (['buffer_pool', 'watermark'], {})
            >>> CLIConverter._xpath_to_path_elems("/interfaces/counters[printall=true]")
            (['interfaces', 'counters'], {'printall': True})
        """
        options = {}
        
        # Extract options from brackets: [key=value]
        # Pattern matches [key=value] at any position
        option_pattern = r'\[([^=\]]+)=([^\]]+)\]'
        matches = re.findall(option_pattern, xpath)
        for key, value in matches:
            # Convert string values to appropriate types
            key = key.strip()
            value = value.strip()
            if value.lower() == 'true':
                options[key] = True
            elif value.lower() == 'false':
                options[key] = False
            elif value.isdigit():
                options[key] = int(value)
            else:
                options[key] = value
        
        # Remove options from xpath to get clean path
        clean_xpath = re.sub(option_pattern, '', xpath)
        
        # Remove leading/trailing slashes and split
        path = clean_xpath.strip("/")
        if not path:
            return [], options
        return path.split("/"), options
    
    @staticmethod
    def _command_to_path_elems(command: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        Convert show command string to path_elems list and options dict.
        
        Args:
            command: Show command string, e.g. "show interfaces counters --printall --period=5"
                     Path parameters (like interface names) are part of the path:
                     "show interfaces errors Ethernet0" -> ["interfaces", "errors", "Ethernet0"]
        
        Returns:
            Tuple of (path_elems, options)
            - path_elems: e.g. ["interfaces", "counters"]
            - options: e.g. {"printall": True, "period": 5}
        
        Examples:
            >>> CLIConverter._command_to_path_elems("show buffer_pool watermark")
            (['buffer_pool', 'watermark'], {})
            >>> CLIConverter._command_to_path_elems("show interfaces counters --printall")
            (['interfaces', 'counters'], {'printall': True})
            >>> CLIConverter._command_to_path_elems("show interfaces errors Ethernet0")
            (['interfaces', 'errors', 'Ethernet0'], {})
        """
        options = {}
        path_parts = []
        
        parts = command.strip().split()
        # Remove "show" prefix if present
        if parts and parts[0].lower() == "show":
            parts = parts[1:]
        
        for part in parts:
            if part.startswith("--"):
                # Parse option: --key=value or --flag
                opt = part[2:]  # Remove --
                if "=" in opt:
                    key, value = opt.split("=", 1)
                    # Convert string values to appropriate types
                    if value.lower() == 'true':
                        options[key] = True
                    elif value.lower() == 'false':
                        options[key] = False
                    elif value.isdigit():
                        options[key] = int(value)
                    else:
                        options[key] = value
                else:
                    # Flag without value, treat as True
                    options[opt] = True
            else:
                path_parts.append(part)
        
        return path_parts, options
    
    def convert(
        self,
        json_data: Any,
        *,
        path_elems: Optional[List[str]] = None,
        xpath: Optional[str] = None,
        command: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Convert GNMI JSON to CLI format text.
        
        Must provide exactly one of: path_elems, xpath, or command.
        
        Args:
            json_data: JSON data returned by GNMI (already parsed to Python object)
            path_elems: Path element list, e.g. ["interfaces", "counters"]
                        or with path parameter: ["interfaces", "errors", "Ethernet0"]
            xpath: XPath string, e.g. "/interfaces/counters"
                   or with path parameter: "/interfaces/errors/Ethernet0"
                   or with options: "/interfaces/counters[printall=true]"
            command: CLI command string, e.g. "show interfaces counters"
                     or with path parameter: "show interfaces errors Ethernet0"
                     or with options: "show interfaces counters --printall"
            options: Optional dict of options, used with path_elems.
                     e.g. {"printall": True}
        
        Returns:
            CLI format text output
        
        Raises:
            PathNotFoundError: Path not supported
            RenderError: Rendering failed
        """
        # Validate: exactly one path specifier must be provided
        specifiers = [path_elems is not None, xpath is not None, command is not None]
        if sum(specifiers) != 1:
            raise ValueError(
                "Must provide exactly one of: path_elems, xpath, or command"
            )
        
        # Convert to path_elems (internal canonical format) and extract options
        if xpath is not None:
            path_elems, final_options = self._xpath_to_path_elems(xpath)
        elif command is not None:
            path_elems, final_options = self._command_to_path_elems(command)
        else:
            final_options = options or {}
        
        try:
            # 1. Find render function
            log.log_debug(f"Looking up renderer for path: {path_elems}")
            render_func = get_renderer(path_elems)
            
            # 2. Call render function with options
            log.log_debug(f"Rendering JSON data for path: {path_elems}, options: {final_options}")
            output = render_func(json_data, path_elems, final_options)
            
            log.log_debug(f"Successfully rendered path: {path_elems}")
            return output
        
        except PathNotFoundError:
            log.log_warning(f"Path not found: {path_elems}")
            raise
        
        except Exception as e:
            log.log_error(f"Failed to render path {path_elems}: {e}")
            raise RenderError(f"Failed to render path {path_elems}: {e}") from e
    
    def is_supported(
        self,
        *,
        path_elems: Optional[List[str]] = None,
        xpath: Optional[str] = None,
        command: Optional[str] = None
    ) -> bool:
        """
        Check if the path is supported.
        
        Must provide exactly one of: path_elems, xpath, or command.
        
        Args:
            path_elems: Path element array
            xpath: XPath string
            command: Show command string
        
        Returns:
            True if supported, False otherwise
        """
        # Convert to path_elems
        if xpath is not None:
            path_elems, _ = self._xpath_to_path_elems(xpath)
        elif command is not None:
            path_elems, _ = self._command_to_path_elems(command)
        elif path_elems is None:
            return False
        
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
