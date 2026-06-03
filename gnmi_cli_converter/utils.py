"""
Render Helper Functions

Provides common rendering pattern helper functions to avoid duplicate code.
"""

from typing import List, Tuple, Dict, Any, Optional


def passthrough(json_data: dict, key: str = "output") -> str:
    """
    Passthrough render - directly return string value.
    
    Applicable for simple commands like show clock, show uptime, etc.
    
    Args:
        json_data: JSON data
        key: Key name to extract, default "output"
    
    Returns:
        String value
    
    Example:
        >>> passthrough({"output": "Thu Jan 23 10:30:00 UTC 2026"})
        'Thu Jan 23 10:30:00 UTC 2026'
    """
    return json_data.get(key, "")


def tabulate_dict(
    rows: List[Tuple],
    headers: List[str],
    title: Optional[str] = None,
    tablefmt: str = "simple",
    stralign: str = "left"
) -> str:
    """
    Table render - using tabulate library.
    
    Applicable for most table output commands.
    
    Args:
        rows: Table row data (list of tuples)
        headers: Header list
        title: Optional title (displayed above table)
        tablefmt: tabulate table format, default "simple"
        stralign: String alignment, default "left"
    
    Returns:
        Formatted table string
    
    Example:
        >>> rows = [("pool1", "12345"), ("pool2", "67890")]
        >>> headers = ["Pool", "Bytes"]
        >>> print(tabulate_dict(rows, headers, title="Watermark:"))
        Watermark:
        Pool    Bytes
        ------  -----
        pool1   12345
        pool2   67890
    """
    from tabulate import tabulate
    
    output = tabulate(rows, headers=headers, tablefmt=tablefmt, stralign=stralign)
    if title:
        output = f"{title}\n{output}"
    return output


def key_value_pairs(json_data: Dict[str, Any], mapping: Dict[str, str]) -> str:
    """
    Key-value pair render.
    
    Applicable for key-value output like show mmu, show processes, etc.
    
    Args:
        json_data: JSON data
        mapping: Field mapping (JSON key -> display name)
    
    Returns:
        Key-value pair formatted string
    
    Example:
        >>> data = {"mmu_size": "12345678", "cell_size": "256"}
        >>> mapping = {"mmu_size": "MMU Size", "cell_size": "Cell Size"}
        >>> print(key_value_pairs(data, mapping))
        MMU Size: 12345678
        Cell Size: 256
    """
    lines = []
    for json_key, display_name in mapping.items():
        value = json_data.get(json_key, "N/A")
        lines.append(f"{display_name}: {value}")
    return "\n".join(lines)
