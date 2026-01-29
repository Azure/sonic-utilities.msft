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

from show_gnmi_util.formatter import ShowVersionFormatter, ShowVlanBriefFormatter, ShowClockFormatter, ShowClockTimezonesFormatter


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


class TestShowClockFormatter(unittest.TestCase):
    """Test cases for ShowClockFormatter"""
    
    def setUp(self):
        self.formatter = ShowClockFormatter()
        self.sample_data = {
            "date": "Wed Jan 28 08:11:13 AM UTC 2026"
        }
    
    def test_format_basic(self):
        """Test basic clock formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertEqual(output, "Wed Jan 28 08:11:13 AM UTC 2026")
    
    def test_format_empty_date(self):
        """Test formatting with missing date"""
        output = self.formatter.format({})
        self.assertEqual(output, "")
    
    def test_format_different_date(self):
        """Test formatting with different date string"""
        data = {"date": "Mon Dec 25 12:00:00 PM PST 2025"}
        output = self.formatter.format(data)
        self.assertEqual(output, "Mon Dec 25 12:00:00 PM PST 2025")


class TestShowClockTimezonesFormatter(unittest.TestCase):
    """Test cases for ShowClockTimezonesFormatter"""
    
    def setUp(self):
        self.formatter = ShowClockTimezonesFormatter()
        self.sample_data = {
            "timezones": [
                "Africa/Abidjan",
                "Africa/Accra",
                "Africa/Addis_Ababa",
                "America/New_York",
                "Europe/London"
            ]
        }
    
    def test_format_basic(self):
        """Test basic timezones formatting"""
        output = self.formatter.format(self.sample_data)
        self.assertIn("Africa/Abidjan", output)
        self.assertIn("America/New_York", output)
        self.assertIn("Europe/London", output)
    
    def test_format_empty_timezones(self):
        """Test formatting with empty timezone list"""
        output = self.formatter.format({"timezones": []})
        self.assertEqual(output, "No timezones configured")
    
    def test_format_no_timezones_key(self):
        """Test formatting when timezones key is missing"""
        output = self.formatter.format({})
        self.assertEqual(output, "No timezones configured")
    
    def test_format_single_timezone(self):
        """Test formatting with single timezone"""
        data = {"timezones": ["UTC"]}
        output = self.formatter.format(data)
        self.assertIn("UTC", output)


if __name__ == '__main__':
    unittest.main()
