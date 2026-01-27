"""
Formatter for 'show vlan brief' command
"""

from typing import Dict, Any, List
from tabulate import tabulate
from natsort import natsorted
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
        Build VLAN table from JSON data using tabulate
        
        Args:
            vlan_data: Dictionary with VLAN information
            
        Returns:
            Formatted table string
        """
        # Define headers
        headers = ['VLAN', 'IP Address', 'Ports', 'Port Tagging', 'DHCP Helper Address', 'Proxy ARP']
        
        # Prepare rows
        table_data = []
        
        # Use natsorted for natural sorting (Vlan1, Vlan2, Vlan10, Vlan20, etc.)
        for vlan_name in natsorted(vlan_data.keys()):
            vlan_info = vlan_data[vlan_name]
            vlan_id = vlan_info.get('vlan_id', '')
            ip_addresses = vlan_info.get('ip_address', [])
            ports_list = vlan_info.get('ports', [])
            dhcp_helpers = vlan_info.get('dhcp_helper_addresses', [])
            proxy_arp = vlan_info.get('proxy_arp', 'disabled')
            
            # Format IP addresses and DHCP helpers
            ip_addr_str = ', '.join(ip_addresses) if ip_addresses else ''
            dhcp_helper_str = ', '.join(dhcp_helpers) if dhcp_helpers else ''
            
            # Handle multiple ports - create separate rows for each port
            if not ports_list:
                table_data.append([
                    vlan_id,
                    ip_addr_str,
                    '',
                    '',
                    dhcp_helper_str,
                    proxy_arp
                ])
            else:
                for idx, port_info in enumerate(ports_list):
                    port_name = port_info.get('name', '')
                    port_tagging = port_info.get('port_tagging', 'untagged')
                    
                    if idx == 0:
                        # First row shows VLAN ID and all info
                        table_data.append([
                            vlan_id,
                            ip_addr_str,
                            port_name,
                            port_tagging,
                            dhcp_helper_str,
                            proxy_arp
                        ])
                    else:
                        # Subsequent rows only show port info
                        table_data.append([
                            '',
                            '',
                            port_name,
                            port_tagging,
                            '',
                            ''
                        ])
        
        # Use tabulate with 'simple' format (includes separator line)
        return tabulate(table_data, headers=headers, tablefmt='simple', stralign='left')
