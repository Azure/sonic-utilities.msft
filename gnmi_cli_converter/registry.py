"""
Command Registry

Provides @register decorator and command lookup functionality.
"""

from typing import List, Callable, Any, Dict
from dataclasses import dataclass
from .exceptions import PathNotFoundError

# Global registry
_REGISTRY: Dict[str, 'CommandEntry'] = {}


@dataclass
class CommandEntry:
    """Command registry entry"""
    path_pattern: List[str]                                      # Registration pattern: ["interfaces", "errors", "*"]
    render_func: Callable[[Any, List[str], Dict[str, Any]], str]  # Render function (unified signature with options)
    command: str                                                  # "show interfaces errors <interface>"


def register(path_pattern: List[str]):
    """
    Decorator: Register render function.
    
    All render functions use a unified signature:
        def render_func(json_data: Any, path_elems: List[str], options: Dict[str, Any]) -> str
    
    Usage:
        # Command without parameters (path_elems and options can be ignored)
        @register(["buffer_pool", "watermark"])
        def render_buffer_pool_watermark(json_data, path_elems, options):
            ...
        
        # Command with parameters (use * to indicate parameter position)
        @register(["interfaces", "errors", "*"])
        def render_interfaces_errors(json_data, path_elems, options):
            interface = path_elems[2]  # Extract parameter
            is_printall = options.get("printall", False)
            ...
    
    Args:
        path_pattern: Path pattern, use "*" to indicate parameter position
    """
    def decorator(func: Callable[[Any, List[str]], str]):
        key = "/".join(path_pattern)
        
        # Generate command description
        cmd_parts = []
        for elem in path_pattern:
            if elem == "*":
                cmd_parts.append("<param>")
            else:
                cmd_parts.append(elem)
        
        _REGISTRY[key] = CommandEntry(
            path_pattern=path_pattern,
            render_func=func,
            command=f"show {' '.join(cmd_parts)}"
        )
        return func
    return decorator


def get_renderer(path_elems: List[str]) -> Callable[[Any, List[str], Dict[str, Any]], str]:
    """
    Find render function.
    
    Args:
        path_elems: Full path, e.g. ["interfaces", "errors", "Ethernet0"]
    
    Returns:
        Render function with signature: (json_data, path_elems, options) -> str
    
    Raises:
        PathNotFoundError: If path is not registered
    
    Matching strategy:
        1. Exact match: interfaces/errors/Ethernet0
        2. Wildcard match: interfaces/errors/*
    """
    # 1. Try exact match
    exact_key = "/".join(path_elems)
    if exact_key in _REGISTRY:
        return _REGISTRY[exact_key].render_func
    
    # 2. Try wildcard match (replace last element with *)
    if len(path_elems) > 0:
        wildcard_key = "/".join(path_elems[:-1] + ["*"])
        if wildcard_key in _REGISTRY:
            return _REGISTRY[wildcard_key].render_func
    
    raise PathNotFoundError(path_elems)


def is_supported(path_elems: List[str]) -> bool:
    """
    Check if the path is supported.
    
    Args:
        path_elems: Path element array
    
    Returns:
        True if supported, False otherwise
    """
    try:
        get_renderer(path_elems)
        return True
    except PathNotFoundError:
        return False


def list_commands() -> List[CommandEntry]:
    """
    List all registered commands.
    
    Returns:
        List of command entries
    """
    return list(_REGISTRY.values())


def clear_registry():
    """
    Clear the registry (for testing only).
    """
    _REGISTRY.clear()
