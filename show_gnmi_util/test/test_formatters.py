"""
Unit tests for formatters
"""

import unittest
import json
from pathlib import Path
import sys

# Add parent directory to path
test_dir = Path(__file__).parent
parent_dir = test_dir.parent.parent
sys.path.insert(0, str(parent_dir))

from show_gnmi_util.formatter import ShowVersionFormatter, ShowVlanBriefFormatter, ShowRebootCauseFormatter, ShowRebootCauseHistoryFormatter


class TestShowVersionFormatter(unittest.TestCase):
    """Test cases for ShowVersionFormatter"""
    
    def setUp(self):
        self.formatter = ShowVersionFormatter()
        self.sample_data = {
            "sonic_software_version": "SONiC.test_branch.1-a8fbac59d",
            "sonic_os_version": "<nil>",
            "distribution": "Debian 11.4",
            "kernel": "5.10.0-18-2-amd64",
            "build_commit": "a8fbac59d",
            "platform": "test_platform",
            "asic": "mellanox",
            "asic_count": "1"
        }
    
    def test_format_basic(self):
        """Test basic formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("SONiC Software Version", output)
        self.assertIn("SONiC.test_branch.1-a8fbac59d", output)
        self.assertIn("Debian 11.4", output)
    
    def test_format_with_docker_images(self):
        """Test formatting with docker images"""
        data = self.sample_data.copy()
        data['docker_images'] = [
            {
                "Repository": "docker-test",
                "Tag": "latest",
                "ID": "sha256:1234567890ab",
                "Size": "100MB"
            }
        ]
        output = self.formatter.format(data)
        self.assertIn("Docker images:", output)
        self.assertIn("docker-test", output)
    
    def test_nil_values(self):
        """Test handling of nil values"""
        output = self.formatter.format(self.sample_data)
        # Should not show <nil> in output
        self.assertNotIn("<nil>", output)


class TestShowVlanBriefFormatter(unittest.TestCase):
    """Test cases for ShowVlanBriefFormatter"""
    
    def setUp(self):
        self.formatter = ShowVlanBriefFormatter()
        self.sample_data = {
            "Vlan1": {
                "dhcp_helper_addresses": ["192.0.0.1"],
                "ip_address": ["192.168.0.1/21"],
                "ports": [
                    {
                        "name": "Ethernet120",
                        "port_tagging": "untagged"
                    }
                ],
                "proxy_arp": "disabled",
                "vlan_id": "1"
            }
        }
    
    def test_format_basic(self):
        """Test basic VLAN formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("VLAN", output)
        self.assertIn("Ethernet120", output)
        self.assertIn("untagged", output)
    
    def test_empty_data(self):
        """Test formatting with empty data"""
        output = self.formatter.format({})
        self.assertIn("No VLANs configured", output)
    
    def test_multiple_ports(self):
        """Test formatting with multiple ports"""
        data = {
            "Vlan2": {
                "vlan_id": "2",
                "ports": [
                    {"name": "Ethernet0", "port_tagging": "tagged"},
                    {"name": "Ethernet4", "port_tagging": "untagged"}
                ],
                "proxy_arp": "enabled"
            }
        }
        output = self.formatter.format(data)
        self.assertIn("Ethernet0", output)
        self.assertIn("Ethernet4", output)


class TestShowRebootCauseFormatter(unittest.TestCase):
    """Test cases for ShowRebootCauseFormatter"""
    
    def setUp(self):
        self.formatter = ShowRebootCauseFormatter()
        self.sample_data = {
            "gen_time": "2025_07_08_18_29_38",
            "cause": "reboot",
            "user": "admin",
            "time": "Tue Jul  8 06:28:26 PM UTC 2025",
            "comment": "N/A"
        }
    
    def test_format_basic(self):
        """Test basic reboot cause formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("Previous reboot cause:", output)
        self.assertIn("Generation Time", output)
        self.assertIn("2025_07_08_18_29_38", output)
        self.assertIn("Cause", output)
        self.assertIn("reboot", output)
        self.assertIn("User", output)
        self.assertIn("admin", output)
    
    def test_format_with_na_values(self):
        """Test formatting with N/A values"""
        data = {
            "gen_time": "2025_07_08_11_53_50",
            "cause": "Hardware - Other (gpi-2, description: gpi 2 detailed fault, time: 2025-07-08 11:53:04)",
            "user": "N/A",
            "time": "N/A",
            "comment": "Unknown"
        }
        output = self.formatter.format(data)
        self.assertIn("Hardware - Other", output)
        self.assertIn("User: N/A", output)
        self.assertIn("Time: N/A", output)
    
    def test_empty_data(self):
        """Test formatting with empty data"""
        output = self.formatter.format({})
        self.assertIn("No reboot cause information available", output)
    
    def test_missing_fields(self):
        """Test formatting with missing fields"""
        data = {"cause": "power-on"}
        output = self.formatter.format(data)
        self.assertIn("Cause: power-on", output)
        self.assertIn("User: N/A", output)
        self.assertIn("Time: N/A", output)


class TestShowRebootCauseHistoryFormatter(unittest.TestCase):
    """Test cases for ShowRebootCauseHistoryFormatter"""
    
    def setUp(self):
        self.formatter = ShowRebootCauseHistoryFormatter()
        self.sample_data = {
            "2025_07_07_02_35_26": {
                "cause": "reboot",
                "comment": "N/A",
                "time": "Mon Jul  7 02:34:07 AM UTC 2025",
                "user": "admin"
            },
            "2025_07_08_09_21_21": {
                "cause": "reboot",
                "comment": "N/A",
                "time": "Tue Jul  8 09:20:13 AM UTC 2025",
                "user": ""
            },
            "2025_07_08_11_53_50": {
                "cause": "Hardware - Other (gpi-2, description: gpi 2 detailed fault, time: 2025-07-08 11:53:04)",
                "comment": "Unknown",
                "time": "N/A",
                "user": "N/A"
            }
        }
    
    def test_format_basic(self):
        """Test basic reboot cause history formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("Name", output)
        self.assertIn("Cause", output)
        self.assertIn("Time", output)
        self.assertIn("User", output)
        self.assertIn("Comment", output)
        self.assertIn("2025_07_07_02_35_26", output)
        self.assertIn("admin", output)
    
    def test_format_with_hardware_fault(self):
        """Test formatting with complex hardware fault description"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("Hardware - Other", output)
        self.assertIn("gpi-2", output)
        self.assertIn("Unknown", output)
    
    def test_format_with_empty_user(self):
        """Test formatting with empty user field"""
        output = self.formatter.format(self.sample_data)
        # Should show N/A for empty user field
        self.assertIn("N/A", output)
    
    def test_empty_data(self):
        """Test formatting with empty data"""
        output = self.formatter.format({})
        self.assertIn("No reboot cause history available", output)
    
    def test_single_entry(self):
        """Test formatting with single entry"""
        data = {
            "2025_07_08_18_29_38": {
                "cause": "reboot",
                "comment": "N/A",
                "time": "Tue Jul  8 06:28:26 PM UTC 2025",
                "user": "admin"
            }
        }
        output = self.formatter.format(data)
        self.assertIn("2025_07_08_18_29_38", output)
        self.assertIn("reboot", output)
        self.assertIn("admin", output)


if __name__ == '__main__':
    unittest.main()

