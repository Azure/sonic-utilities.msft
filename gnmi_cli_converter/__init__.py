"""
GNMI CLI Converter

A framework for converting GNMI JSON to CLI format output.

Main interfaces:
- CLIConverter: Main converter class
- CommandInfo: Command information dataclass

Usage example:
    >>> from gnmi_cli_converter import CLIConverter
    >>> converter = CLIConverter()
    >>> json_data = {
    ...     "egress_lossless_pool": {"Bytes": "12345"},
    ...     "ingress_lossless_pool": {"Bytes": "67890"}
    ... }
    >>> output = converter.convert(["buffer_pool", "watermark"], json_data)
    >>> print(output)
    Shared pool maximum occupancy:
                     Pool  Bytes
    ---------------------  -----
      egress_lossless_pool  12345
     ingress_lossless_pool  67890
"""

# Import commands module to trigger all command registrations
from . import commands

# Export main interfaces
from .converter import CLIConverter, CommandInfo
from .exceptions import (
    CLIConverterError,
    PathNotFoundError,
    InvalidJSONError,
    RenderError,
    MissingFieldError
)

__all__ = [
    'CLIConverter',
    'CommandInfo',
    'CLIConverterError',
    'PathNotFoundError',
    'InvalidJSONError',
    'RenderError',
    'MissingFieldError',
]

__version__ = '1.0.0'
