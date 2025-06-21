# Error definitions for the validation library

class ValidationError(Exception):
    """
    Custom exception for validation errors with field path support.
    Provides detailed error information including the field path and custom messages.
    """
    def __init__(self, message: str, field: str = None, path: list[str] = None):
        """
        Initialize a validation error with message and optional field information.
        
        Args:
            message: Human-readable error message
            field: The specific field that failed validation
            path: List of field names leading to the error (for nested validation)
        """
        self.message = message
        self.field = field
        self.path = path or []  # Default to empty list if no path provided
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """
        Return a formatted error message with field path if available.
        
        Returns:
            Formatted error string with path context
        """
        if self.path:
            path_str = " -> ".join(self.path)  # Join path elements with arrows
            return f"{path_str}: {self.message}"
        return self.message 