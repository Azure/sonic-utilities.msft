"""
Base formatter class for converting JSON to tabular format
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseFormatter(ABC):
    """
    Abstract base class for all formatters
    """
    
    def __init__(self):
        self.output_lines = []
    
    @abstractmethod
    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert JSON data to tabular format
        
        Args:
            json_data: Dictionary containing the JSON data
            
        Returns:
            Formatted string in tabular format
        """
        pass
    
    def _add_line(self, line: str = ""):
        """Add a line to the output"""
        self.output_lines.append(line)
    
    def _add_separator(self):
        """Add a separator line"""
        self._add_line()
    
    def _add_header(self, title: str):
        """Add a header with underline"""
        self._add_line(title)
        self._add_line()
    
    def _format_key_value(self, key: str, value: str, separator: str = ": ") -> str:
        """Format a key-value pair"""
        return f"{key}{separator}{value}"
    
    def _get_output(self) -> str:
        """Get the formatted output as a string"""
        return "\n".join(self.output_lines)
    
    def _clear_output(self):
        """Clear the output buffer"""
        self.output_lines = []
