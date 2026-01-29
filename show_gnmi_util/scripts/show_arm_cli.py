#!/usr/bin/env python3
"""
CLI tool to read JSON files and convert them to tabular format
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
script_dir = Path(__file__).parent
parent_dir = script_dir.parent.parent
sys.path.insert(0, str(parent_dir))

from show_gnmi_util.formatter import ShowVersionFormatter, ShowVlanBriefFormatter, ShowRebootCauseFormatter, ShowRebootCauseHistoryFormatter


def read_json_file(filepath: str) -> dict:
    """
    Read and parse JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data as dictionary
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def format_show_version(json_file: str) -> str:
    """
    Format show version JSON to tabular format
    
    Args:
        json_file: Path to show version JSON file
        
    Returns:
        Formatted tabular output
    """
    json_data = read_json_file(json_file)
    formatter = ShowVersionFormatter()
    return formatter.format(json_data)


def format_show_vlan_brief(json_file: str) -> str:
    """
    Format show vlan brief JSON to tabular format
    
    Args:
        json_file: Path to show vlan brief JSON file
        
    Returns:
        Formatted tabular output
    """
    json_data = read_json_file(json_file)
    formatter = ShowVlanBriefFormatter()
    return formatter.format(json_data)


def format_show_reboot_cause(json_file: str) -> str:
    """
    Format show reboot cause JSON to tabular format
    
    Args:
        json_file: Path to reboot cause JSON file
        
    Returns:
        Formatted tabular output
    """
    json_data = read_json_file(json_file)
    formatter = ShowRebootCauseFormatter()
    return formatter.format(json_data)


def format_show_reboot_cause_history(json_file: str) -> str:
    """
    Format show reboot cause history JSON to tabular format
    
    Args:
        json_file: Path to reboot cause history JSON file
        
    Returns:
        Formatted tabular output
    """
    json_data = read_json_file(json_file)
    formatter = ShowRebootCauseHistoryFormatter()
    return formatter.format(json_data)


def main():
    """
    Main function to demonstrate formatters
    """
    script_dir = Path(__file__).parent
    
    # File paths
    version_json = script_dir / "show_version_sample.json"
    vlan_json = script_dir / "show_vlan_brief_sample.json"
    reboot_cause_json = script_dir / "show_reboot_cause_sample.json"
    reboot_cause_history_json = script_dir / "show_reboot_cause_history_sample.json"
    
    # Format and display show version
    print("=" * 80)
    print("SHOW VERSION")
    print("=" * 80)
    version_output = format_show_version(str(version_json))
    print(version_output)
    print()
    
    # Format and display show vlan brief
    print("=" * 80)
    print("SHOW VLAN BRIEF")
    print("=" * 80)
    vlan_output = format_show_vlan_brief(str(vlan_json))
    print(vlan_output)
    print()
    
    # Format and display show reboot cause
    print("=" * 80)
    print("SHOW REBOOT CAUSE")
    print("=" * 80)
    reboot_cause_output = format_show_reboot_cause(str(reboot_cause_json))
    print(reboot_cause_output)
    print()
    
    # Format and display show reboot cause history
    print("=" * 80)
    print("SHOW REBOOT CAUSE HISTORY")
    print("=" * 80)
    reboot_cause_history_output = format_show_reboot_cause_history(str(reboot_cause_history_json))
    print(reboot_cause_history_output)
    print()
    
    # Return all outputs for programmatic use
    return {
        'show_version': version_output,
        'show_vlan_brief': vlan_output,
        'show_reboot_cause': reboot_cause_output,
        'show_reboot_cause_history': reboot_cause_history_output
    }


if __name__ == "__main__":
    main()

