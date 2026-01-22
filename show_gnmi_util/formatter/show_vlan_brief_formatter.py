"""
Formatter for 'show vlan brief' command
"""

from typing import Dict, Any, List
from ..common.base_formatter import BaseFormatter


class ShowVlanBriefFormatter(BaseFormatter):
    """
    Format 'show vlan brief' JSON output to tabular format
    """
    
    def format(self, json_data: Dict[str, Any]) -> str:
        """
        Convert show vlan brief JSON to tabular format
        
        Args:
            json_data: Dictionary containing VLAN data
            
        Returns:
            Formatted string in tabular format
        """
        self._clear_output()
        
        if not json_data:
            return "No VLANs configured"
        
        # Build table
        table_output = self._build_vlan_table(json_data)
        self._add_line(table_output)
        
        return self._get_output()
    
    def _build_vlan_table(self, vlan_data: Dict[str, Any]) -> str:
        """
        Build VLAN table from JSON data
        
        Args:
            vlan_data: Dictionary with VLAN information
            
        Returns:
            Formatted table string
        """
        # Define headers
        headers = ['VLAN', 'IP Address', 'Ports', 'Port Tagging', 'DHCP Helper Address', 'Proxy ARP']
        
        # Calculate column widths
        col_widths = {
            'VLAN': len('VLAN'),
            'IP Address': len('IP Address'),
            'Ports': len('Ports'),
            'Port Tagging': len('Port Tagging'),
            'DHCP Helper Address': len('DHCP Helper Address'),
            'Proxy ARP': len('Proxy ARP')
        }
        
        # Prepare rows
        rows = []
        for vlan_name, vlan_info in sorted(vlan_data.items()):
            vlan_id = vlan_info.get('vlan_id', '')
            ip_addresses = vlan_info.get('ip_address', [])
            ports_list = vlan_info.get('ports', [])
            dhcp_helpers = vlan_info.get('dhcp_helper_addresses', [])
            proxy_arp = vlan_info.get('proxy_arp', 'disabled')
            
            # Handle multiple ports - create separate rows for each port
            if not ports_list:
                row = {
                    'VLAN': vlan_id,
                    'IP Address': ', '.join(ip_addresses) if ip_addresses else '',
                    'Ports': '',
                    'Port Tagging': '',
                    'DHCP Helper Address': ', '.join(dhcp_helpers) if dhcp_helpers else '',
                    'Proxy ARP': proxy_arp
                }
                rows.append(row)
            else:
                for idx, port_info in enumerate(ports_list):
                    port_name = port_info.get('name', '')
                    port_tagging = port_info.get('port_tagging', 'untagged')
                    
                    if idx == 0:
                        # First row shows VLAN ID and all info
                        row = {
                            'VLAN': vlan_id,
                            'IP Address': ', '.join(ip_addresses) if ip_addresses else '',
                            'Ports': port_name,
                            'Port Tagging': port_tagging,
                            'DHCP Helper Address': ', '.join(dhcp_helpers) if dhcp_helpers else '',
                            'Proxy ARP': proxy_arp
                        }
                    else:
                        # Subsequent rows only show port info
                        row = {
                            'VLAN': '',
                            'IP Address': '',
                            'Ports': port_name,
                            'Port Tagging': port_tagging,
                            'DHCP Helper Address': '',
                            'Proxy ARP': ''
                        }
                    rows.append(row)
            
            # Update column widths
            for row in rows:
                for key, value in row.items():
                    col_widths[key] = max(col_widths[key], len(str(value)))
        
        # Build table output
        table_lines = []
        
        # Create separator line
        separator = '-' * (sum(col_widths.values()) + 3 * (len(headers) - 1))
        
        # Header
        header_line = '   '.join([header.ljust(col_widths[header]) for header in headers])
        table_lines.append(header_line)
        table_lines.append(separator)
        
        # Data rows
        for row in rows:
            data_line = '   '.join([str(row[header]).ljust(col_widths[header]) for header in headers])
            table_lines.append(data_line)
        
        return '\n'.join(table_lines)
