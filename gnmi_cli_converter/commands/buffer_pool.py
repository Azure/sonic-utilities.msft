"""
Buffer Pool Related Command Render Functions

Contains:
- show buffer_pool watermark
- show buffer_pool persistent-watermark
"""

from typing import Any, List
from natsort import natsorted
from ..utils import tabulate_dict
from ..registry import register


@register(["buffer_pool", "watermark"])
def render_buffer_pool_watermark(json_data: Any, path_elems: List[str]) -> str:
    """
    show buffer_pool watermark
    
    Args:
        json_data: JSON data returned by GNMI
        path_elems: Path element array (not used by this command)
    
    Input JSON example:
        {
            "egress_lossless_pool": {"Bytes": "12345"},
            "egress_lossy_pool": {"Bytes": "67890"},
            "ingress_lossless_pool": {"Bytes": "24680"}
        }
    
    Output example:
        Shared pool maximum occupancy:
                         Pool  Bytes
        ---------------------  -----
          egress_lossless_pool  12345
             egress_lossy_pool  67890
        ingress_lossless_pool  24680
    """
    if not json_data:
        return "Shared pool maximum occupancy:\nNo data available"
    
    # Use natsorted for natural sorting
    rows = [
        (pool, data.get("Bytes", "N/A")) 
        for pool, data in natsorted(json_data.items())
    ]
    
    return tabulate_dict(
        title="Shared pool maximum occupancy:",
        headers=["Pool", "Bytes"],
        rows=rows,
        stralign="right"
    )


@register(["buffer_pool", "persistent-watermark"])
def render_buffer_pool_persistent_watermark(json_data: Any, path_elems: List[str]) -> str:
    """
    show buffer_pool persistent-watermark
    
    Format is the same as watermark, only the data source is different.
    
    Args:
        json_data: JSON data returned by GNMI
        path_elems: Path element array (not used by this command)
    """
    if not json_data:
        return "Shared pool maximum occupancy:\nNo data available"
    
    rows = [
        (pool, data.get("Bytes", "N/A")) 
        for pool, data in natsorted(json_data.items())
    ]
    
    return tabulate_dict(
        title="Shared pool maximum occupancy:",
        headers=["Pool", "Bytes"],
        rows=rows,
        stralign="right"
    )
