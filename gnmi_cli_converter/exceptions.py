"""
CLI Converter Custom Exception Classes
"""


class CLIConverterError(Exception):
    """CLI Converter base exception"""
    pass


class PathNotFoundError(CLIConverterError):
    """Path not registered"""
    def __init__(self, path_elems):
        self.path_elems = path_elems
        super().__init__(f"Path not registered: {path_elems}")


class InvalidJSONError(CLIConverterError):
    """Invalid JSON data"""
    pass


class RenderError(CLIConverterError):
    """Render failed"""
    pass


class MissingFieldError(CLIConverterError):
    """Required field missing"""
    pass
