"""
Formatter for 'show version' command
"""

from typing import Dict, Any, List
from tabulate import tabulate
from ..common.base_formatter import BaseFormatter


class ShowVersionFormatter(BaseFormatter):
    """
    Format 'show version' JSON output to tabular format
    """
    
    def __init__(self):
        super().__init__()
        self.field_mappings = {
            'sonic_software_version': 'SONiC Software Version',
            'sonic_os_version': 'SONiC OS Version',
            'distribution': 'Distribution',
            'kernel': 'Kernel',
            'build_commit': 'Build commit',
            'build_date': 'Build date',
            'built_by': 'Built by',
            'platform': 'Platform',
            'hwsku': 'HwSKU',
            'asic': 'ASIC',
            'asic_count': 'ASIC Count',
            'serial_number': 'Serial Number',
            'model_number': 'Model Number',
            'hardware_revision': 'Hardware Revision',
            'uptime': 'Uptime',
            'date': 'Date'
        }
    
    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show version JSON to tabular format
        
        Args:
            json_data: Dictionary containing show version data
            
        Returns:
            Formatted string in tabular format
        """
        self._clear_output()
        
        # Add main version information
        for json_key, display_name in self.field_mappings.items():
            value = json_data.get(json_key, '')
            
            # Handle special cases
            if value in ['<nil>', '\u003cnil\u003e', None]:
                value = ''
            
            # Skip empty HwSKU
            if json_key == 'hwsku' and not value:
                continue
            
            self._add_line(self._format_key_value(display_name, str(value)))
        
        # Add Docker images section if present
        docker_images = json_data.get('docker_images', [])
        if docker_images:
            self._add_separator()
            self._add_line("Docker images:")
            self._add_line(self._format_docker_table(docker_images))
        
        return self._get_output()
    
    def _format_docker_table(self, docker_images: List[Dict[str, str]]) -> str:
        """
        Format docker images as a table using tabulate
        
        Args:
            docker_images: List of docker image dictionaries
            
        Returns:
            Formatted table string
        """
        if not docker_images:
            return ""
        
        # Prepare table data
        headers = ['REPOSITORY', 'TAG', 'IMAGE ID', 'SIZE']
        table_data = []
        
        for image in docker_images:
            repo = image.get('Repository', '')
            tag = image.get('Tag', '')
            image_id = image.get('ID', '')
            size = image.get('Size', '')
            
            # Extract short image ID (first 12 chars after sha256:)
            if image_id.startswith('sha256:'):
                image_id = image_id[7:19]
            
            table_data.append([repo, tag, image_id, size])
        
        # Use tabulate to format the table
        # 'plain' tablefmt matches the simple format used in show version
        return tabulate(table_data, headers=headers, tablefmt='plain')
