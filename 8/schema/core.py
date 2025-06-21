# Core module containing the main Schema builder class and ValidationError exception
# This module provides the main API for creating and using validators
from .validators import StringValidator, NumberValidator, BooleanValidator, DateValidator, ObjectValidator, ArrayValidator
from .errors import ValidationError  # Import from new errors module

class Schema:
    """
    Main schema builder class with type-safe static methods.
    Provides a fluent API for creating validators for different data types.
    """
    
    @staticmethod
    def string() -> StringValidator:
        """
        Create a string validator for text validation.
        
        Returns:
            StringValidator instance for building string validation rules
        """
        return StringValidator()
    
    @staticmethod
    def number() -> NumberValidator:
        """
        Create a number validator for numeric validation.
        
        Returns:
            NumberValidator instance for building numeric validation rules
        """
        return NumberValidator()
    
    @staticmethod
    def boolean() -> BooleanValidator:
        """
        Create a boolean validator for boolean validation.
        
        Returns:
            BooleanValidator instance for building boolean validation rules
        """
        return BooleanValidator()
    
    @staticmethod
    def date() -> DateValidator:
        """
        Create a date validator for date/time validation.
        
        Returns:
            DateValidator instance for building date validation rules
        """
        return DateValidator()
    
    @staticmethod
    def object(schema: dict[str, 'Validator']) -> ObjectValidator:
        """
        Create an object validator for dictionary/object validation.
        
        Args:
            schema: Dictionary mapping field names to their validators
            
        Returns:
            ObjectValidator instance for validating object structures
        """
        return ObjectValidator(schema)
    
    @staticmethod
    def array(item_validator: 'Validator') -> ArrayValidator:
        """
        Create an array validator for list validation.
        
        Args:
            item_validator: Validator to apply to each item in the array
            
        Returns:
            ArrayValidator instance for validating array structures
        """
        return ArrayValidator(item_validator) 