"""
Formatter for 'show clock' command and 'show clock timezones output.
"""

from typing import List, Dict, Any
from ..common.base_formatter import BaseFormatter

class ShowClockFormatter(BaseFormatter):
    """
    Format 'show clock' JSON output to CLI format
    """

    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show clock JSON to CLI format

        Args:
            json_data: Dictionary containing show clock data

        Returns:
            Formatted string in CLI format

        Example:
        ({"clock": "Wed Jan 28 08:11:13 AM UTC 2026"})
        'Wed Jan 28 08:11:13 AM UTC 2026'

        """
        self._clear_output()

        output = json_data.get('date', '')

        return output
    
class ShowClockTimezonesFormatter(BaseFormatter):
    """
    Format 'show clock timezones' JSON output to tabular format
    """

    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show clock timezones JSON to tabular format

        Args:
            json_data: Dictionary containing show clock timezones data

        Returns:
            Formatted string in tabular format
        """
        self._clear_output()

        timezones = json_data.get('timezones', [])
        if not timezones:
            return "No timezones configured"

        # Prepare table data
        table_data = []
        for tz in timezones:
            table_data._add_line(tz)

        return self._get_output()
    
