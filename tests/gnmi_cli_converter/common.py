"""
Common test helpers for gnmi_cli_converter tests.

Provides utilities for loading test data from files.
"""

import json
from pathlib import Path

# Test data directory
TESTDATA_DIR = Path(__file__).parent / "testdata"
INPUTS_DIR = TESTDATA_DIR / "inputs"
EXPECTED_DIR = TESTDATA_DIR / "expected"


def load_json(filename: str) -> dict:
    """Load JSON test data from inputs directory.
    
    Args:
        filename: Name of the JSON file (e.g., "buffer_pool_watermark.json")
    
    Returns:
        Parsed JSON data as dict
    """
    with open(INPUTS_DIR / filename, 'r') as f:
        return json.load(f)


def load_expected(filename: str) -> str:
    """Load expected output from expected directory.
    
    Args:
        filename: Name of the expected output file (e.g., "buffer_pool_watermark.txt")
    
    Returns:
        Expected output string (trailing newline stripped)
    """
    with open(EXPECTED_DIR / filename, 'r') as f:
        return f.read().rstrip('\n')
