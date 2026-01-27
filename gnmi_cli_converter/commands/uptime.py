"""
Uptime Command Render Function

Contains:
- show uptime
"""

from typing import Any, List
from ..utils import passthrough
from ..registry import register


@register(["uptime"])
def render_uptime(json_data: Any, path_elems: List[str]) -> str:
    """
    show uptime
    
    Args:
        json_data: JSON data returned by GNMI
        path_elems: Path element array (not used by this command)
    
    Input JSON example:
        {"uptime": "up 3 weeks, 4 days, 10 hours, 15 minutes"}
    
    Output example:
        up 3 weeks, 4 days, 10 hours, 15 minutes
    """
    return passthrough(json_data, key="uptime")
