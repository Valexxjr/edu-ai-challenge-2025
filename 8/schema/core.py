from .validators import StringValidator, NumberValidator, BooleanValidator, DateValidator, ObjectValidator, ArrayValidator

class ValidationError(Exception):
    """Custom exception for validation errors with field path support"""
    def __init__(self, message: str, field: str = None, path: list[str] = None):
        self.message = message
        self.field = field
        self.path = path or []
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.path:
            path_str = " -> ".join(self.path)
            return f"{path_str}: {self.message}"
        return self.message

class Schema:
    """Main schema builder class with type-safe static methods"""
    
    @staticmethod
    def string() -> StringValidator:
        """Create a string validator"""
        return StringValidator()
    
    @staticmethod
    def number() -> NumberValidator:
        """Create a number validator"""
        return NumberValidator()
    
    @staticmethod
    def boolean() -> BooleanValidator:
        """Create a boolean validator"""
        return BooleanValidator()
    
    @staticmethod
    def date() -> DateValidator:
        """Create a date validator"""
        return DateValidator()
    
    @staticmethod
    def object(schema: dict[str, 'Validator']) -> ObjectValidator:
        """Create an object validator with nested schema"""
        return ObjectValidator(schema)
    
    @staticmethod
    def array(item_validator: 'Validator') -> ArrayValidator:
        """Create an array validator with item validation"""
        return ArrayValidator(item_validator) 