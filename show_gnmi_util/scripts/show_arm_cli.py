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

from show_gnmi_util.formatter import ShowVersionFormatter, ShowVlanBriefFormatter, ShowClockFormatter, ShowClockTimezonesFormatter


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

def format_show_clock(json_file: str) -> str:
    """
    Format show clock JSON to CLI format
    
    Args:
        json_file: Path to show clock JSON file
        
    Returns:
        Formatted CLI output
    """
    json_data = read_json_file(json_file)
    formatter = ShowClockFormatter()
    return formatter.format(json_data)

def format_show_clock_timezones(json_file: str) -> str:
    """
    Format show clock timezones JSON to tabular format
    
    Args:
        json_file: Path to show clock timezones JSON file
        
    Returns:
        Formatted tabular output
    """
    json_data = read_json_file(json_file)
    formatter = ShowClockTimezonesFormatter()
    return formatter.format(json_data)


def main():
    """
    Main function to demonstrate formatters
    """
    script_dir = Path(__file__).parent
    
    # File paths
    version_json = script_dir / "show_version_sample.json"
    vlan_json = script_dir / "show_vlan_brief_sample.json"
    clock_json = script_dir / "show_clock_sample.json"
    clock_timezones_json = script_dir / "show_clock_timezones_sample.json"

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

    # Format and display show clock
    print("=" * 80)
    print("SHOW CLOCK")
    print("=" * 80)
    clock_output = format_show_clock(str(clock_json))
    print(clock_output)
    print()

    # Format and display show clock timezones
    print("=" * 80)
    print("SHOW CLOCK TIMEZONES")
    print("=" * 80)
    clock_timezones_output = format_show_clock_timezones(str(clock_timezones_json))
    print(clock_timezones_output)
    print()
    
    # Return both outputs for programmatic use
    return {
        'show_version': version_output,
        'show_vlan_brief': vlan_output,
        'show_clock': clock_output,
        'show_clock_timezones': clock_timezones_output
    }


if __name__ == "__main__":
    main()
