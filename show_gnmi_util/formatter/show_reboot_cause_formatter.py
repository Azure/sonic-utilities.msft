"""
Formatters for 'show reboot cause' and 'show reboot cause history' commands
"""

from typing import Dict, Any, List
from tabulate import tabulate
from ..common.base_formatter import BaseFormatter


class ShowRebootCauseFormatter(BaseFormatter):
    """
    Format 'show reboot cause' JSON output to tabular format
    """
    
    def __init__(self):
        super().__init__()
        self.field_mappings = {
            'gen_time': 'Generation Time',
            'cause': 'Cause',
            'user': 'User', 
            'time': 'Time',
            'comment': 'Comment'
        }
    
    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show reboot cause data to tabular format
        
        Args:
            json_data: JSON data containing reboot cause information
            
        Returns:
            Formatted string in tabular format
        """
        self._clear_output()
        
        if not json_data:
            self._add_line("No reboot cause information available")
            return self._get_output()
        
        # Format reboot cause information
        self._add_line("Previous reboot cause:")
        self._add_separator()
        
        for json_key, display_name in self.field_mappings.items():
            value = json_data.get(json_key, 'N/A')
            
            # Handle None, empty values, or "N/A" strings
            if value is None or value == '' or value == 'N/A':
                value = 'N/A'
            
            self._add_line(self._format_key_value(display_name, str(value)))
        
        return self._get_output()


class ShowRebootCauseHistoryFormatter(BaseFormatter):
    """
    Format 'show reboot cause history' JSON output to tabular format
    """
    
    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show reboot cause history data to tabular format
        
        Args:
            json_data: JSON data containing reboot cause history information
            
        Returns:
            Formatted string in tabular format
        """
        self._clear_output()
        
        if not json_data:
            self._add_line("No reboot cause history available")
            return self._get_output()
        
        # Format reboot cause history as table
        table_output = self._build_reboot_history_table(json_data)
        self._add_line(table_output)
        
        return self._get_output()
    
    def _build_reboot_history_table(self, history_data: Dict[str, Any]) -> str:
        """
        Build reboot cause history table from JSON data using tabulate
        
        Args:
            history_data: Dictionary with reboot cause history information
            
        Returns:
            Formatted table string
        """
        # Define headers
        headers = ['Name', 'Cause', 'Time', 'User', 'Comment']
        
        # Prepare rows
        table_data = []
        
        for entry_name, entry_data in history_data.items():
            if isinstance(entry_data, dict):
                cause = entry_data.get('cause', 'N/A')
                time = entry_data.get('time', 'N/A')
                user = entry_data.get('user', 'N/A')
                comment = entry_data.get('comment', 'N/A')
                
                # Handle None, empty values, or "N/A" strings
                cause = 'N/A' if not cause or cause == 'N/A' else str(cause)
                time = 'N/A' if not time or time == 'N/A' else str(time)
                user = 'N/A' if not user or user == 'N/A' else str(user)
                comment = 'N/A' if not comment or comment == 'N/A' else str(comment)
                
                table_data.append([entry_name, cause, time, user, comment])
        
        if not table_data:
            return "No reboot cause history entries found"
        
        # Sort by entry name for consistent output
        table_data.sort(key=lambda x: x[0])
        
        # Use tabulate to format the table
        return tabulate(table_data, headers=headers, tablefmt='simple')
