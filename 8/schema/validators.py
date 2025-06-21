# Schema Builder - Type-Safe Validation Library
# This module contains all the validator classes for different data types
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Protocol, runtime_checkable
from typing_extensions import Self
import re
from datetime import datetime
from abc import ABC, abstractmethod
from .errors import ValidationError  # Import ValidationError for proper exception handling

# Type variables for generic validators
T = TypeVar('T')  # Generic type for validated data
V = TypeVar('V', bound='Validator')  # Type variable bound to Validator class

@runtime_checkable
class ValidatorProtocol(Protocol):
    """
    Protocol defining the interface that all validators must implement.
    This allows for runtime type checking of validator objects.
    """
    def validate(self, value: Any) -> Any: ...  # Validate a value and return the validated result
    def with_message(self, message: str) -> Self: ...  # Set a custom error message

class Validator(ABC):
    """
    Abstract base class for all validators.
    Provides common functionality like optional fields and custom error messages.
    """
    
    def __init__(self) -> None:
        """Initialize the base validator with default settings."""
        self._custom_message: Optional[str] = None  # Custom error message to use instead of default
        self._optional: bool = False  # Whether this field can be None/optional
    
    def with_message(self, message: str) -> Self:
        """
        Set a custom error message for this validator.
        
        Args:
            message: The custom error message to display on validation failure
            
        Returns:
            Self for method chaining
        """
        self._custom_message = message
        return self
    
    def optional(self) -> Self:
        """
        Mark this field as optional (can be None).
        
        Returns:
            Self for method chaining
        """
        self._optional = True
        return self
    
    def _is_optional_and_none(self, value: Any) -> bool:
        """
        Check if the value is None and the field is marked as optional.
        
        Args:
            value: The value to check
            
        Returns:
            True if value is None and field is optional, False otherwise
        """
        return value is None and self._optional
    
    @abstractmethod
    def validate(self, value: Any) -> Any:
        """
        Abstract method that must be implemented by all validator subclasses.
        Validates the given value according to the validator's rules.
        
        Args:
            value: The value to validate
            
        Returns:
            The validated value (may be transformed)
            
        Raises:
            ValidationError: If validation fails
        """
        pass

class StringValidator(Validator):
    """
    Validator for string values with support for length constraints and regex patterns.
    """
    
    def __init__(self) -> None:
        """Initialize string validator with no constraints."""
        super().__init__()
        self._min_length: Optional[int] = None  # Minimum string length requirement
        self._max_length: Optional[int] = None  # Maximum string length requirement
        self._pattern: Optional[str] = None  # Regex pattern string
        self._compiled_pattern: Optional[re.Pattern] = None  # Compiled regex pattern for efficiency
    
    def min_length(self, length: int) -> Self:
        """
        Set the minimum length requirement for strings.
        
        Args:
            length: Minimum number of characters required
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If length is negative
        """
        if length < 0:
            raise ValueError("Minimum length must be non-negative")
        self._min_length = length
        return self
    
    def max_length(self, length: int) -> Self:
        """
        Set the maximum length requirement for strings.
        
        Args:
            length: Maximum number of characters allowed
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If length is negative
        """
        if length < 0:
            raise ValueError("Maximum length must be non-negative")
        self._max_length = length
        return self
    
    def pattern(self, regex: str) -> Self:
        """
        Set a regex pattern that the string must match.
        
        Args:
            regex: Regular expression pattern string
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If the regex pattern is invalid
        """
        try:
            self._pattern = regex
            self._compiled_pattern = re.compile(regex)  # Compile for efficiency
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        return self
    
    def validate(self, value: Any) -> str:
        """
        Validate that the value is a string meeting all constraints.
        
        Args:
            value: The value to validate
            
        Returns:
            The validated string value
            
        Raises:
            ValidationError: If validation fails (wrong type, length, or pattern)
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        # Check if value is a string
        if not isinstance(value, str):
            raise ValidationError(
                self._custom_message or f"Expected string, got {type(value).__name__}"
            )
        
        # Check minimum length constraint
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError(
                self._custom_message or f"String must be at least {self._min_length} characters long"
            )
        
        # Check maximum length constraint
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError(
                self._custom_message or f"String must be at most {self._max_length} characters long"
            )
        
        # Check regex pattern constraint
        if self._compiled_pattern is not None and not self._compiled_pattern.match(value):
            raise ValidationError(
                self._custom_message or f"String does not match pattern {self._pattern}"
            )
        
        return value

class NumberValidator(Validator):
    """
    Validator for numeric values (int and float) with range constraints.
    """
    
    def __init__(self) -> None:
        """Initialize number validator with no constraints."""
        super().__init__()
        self._min_value: Optional[Union[int, float]] = None  # Minimum numeric value
        self._max_value: Optional[Union[int, float]] = None  # Maximum numeric value
        self._integer_only: bool = False  # Whether to only accept integers
    
    def min_value(self, value: Union[int, float]) -> Self:
        """
        Set the minimum value constraint.
        
        Args:
            value: Minimum allowed value
            
        Returns:
            Self for method chaining
        """
        self._min_value = value
        return self
    
    def max_value(self, value: Union[int, float]) -> Self:
        """
        Set the maximum value constraint.
        
        Args:
            value: Maximum allowed value
            
        Returns:
            Self for method chaining
        """
        self._max_value = value
        return self
    
    def integer_only(self) -> Self:
        """
        Restrict validation to integer values only (reject floats).
        
        Returns:
            Self for method chaining
        """
        self._integer_only = True
        return self
    
    def validate(self, value: Any) -> Union[int, float]:
        """
        Validate that the value is a number meeting all constraints.
        
        Args:
            value: The value to validate
            
        Returns:
            The validated numeric value
            
        Raises:
            ValidationError: If validation fails (wrong type, range, or integer constraint)
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        # Check if value is a number
        if not isinstance(value, (int, float)):
            raise ValidationError(
                self._custom_message or f"Expected number, got {type(value).__name__}"
            )
        
        # Check integer-only constraint
        if self._integer_only and not isinstance(value, int):
            raise ValidationError(
                self._custom_message or "Expected integer, got float"
            )
        
        # Check minimum value constraint
        if self._min_value is not None and value < self._min_value:
            raise ValidationError(
                self._custom_message or f"Value must be at least {self._min_value}"
            )
        
        # Check maximum value constraint
        if self._max_value is not None and value > self._max_value:
            raise ValidationError(
                self._custom_message or f"Value must be at most {self._max_value}"
            )
        
        return value

class BooleanValidator(Validator):
    """
    Validator for boolean values with optional strict mode.
    """
    
    def __init__(self) -> None:
        """Initialize boolean validator in strict mode."""
        super().__init__()
        self._strict: bool = True  # Whether to only accept True/False vs truthy/falsy
    
    def strict(self, strict: bool = True) -> Self:
        """
        Set strict mode for boolean validation.
        
        Args:
            strict: If True, only accept True/False. If False, accept truthy/falsy values
            
        Returns:
            Self for method chaining
        """
        self._strict = strict
        return self
    
    def validate(self, value: Any) -> bool:
        """
        Validate that the value is a boolean (or truthy/falsy in non-strict mode).
        
        Args:
            value: The value to validate
            
        Returns:
            The validated boolean value
            
        Raises:
            ValidationError: If validation fails in strict mode
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        if self._strict:
            # Strict mode: only accept actual boolean values
            if not isinstance(value, bool):
                raise ValidationError(
                    self._custom_message or f"Expected boolean, got {type(value).__name__}"
                )
            return value
        else:
            # Non-strict mode: accept any truthy/falsy value
            return bool(value)

class DateValidator(Validator):
    """
    Validator for date values with support for multiple formats.
    """
    
    def __init__(self) -> None:
        """Initialize date validator with ISO and timestamp format support."""
        super().__init__()
        self._formats: List[str] = ['iso', 'timestamp']  # Supported date formats
    
    def formats(self, *formats: str) -> Self:
        """
        Set the accepted date formats.
        
        Args:
            *formats: Variable number of format strings ('iso', 'timestamp', or strptime formats)
            
        Returns:
            Self for method chaining
        """
        self._formats = list(formats)
        return self
    
    def validate(self, value: Any) -> datetime:
        """
        Validate that the value is a valid date in one of the accepted formats.
        
        Args:
            value: The value to validate (string, datetime, or timestamp)
            
        Returns:
            The validated datetime object
            
        Raises:
            ValidationError: If validation fails (unsupported format or invalid date)
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        # If already a datetime object, return it
        if isinstance(value, datetime):
            return value
        
        # Handle string values
        if isinstance(value, str):
            # Try ISO format first
            if 'iso' in self._formats:
                try:
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            # Try other custom formats
            for fmt in self._formats:
                if fmt != 'iso':
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
        
        # Handle timestamp values (int/float)
        elif isinstance(value, (int, float)) and 'timestamp' in self._formats:
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                pass
        
        # If we get here, no format worked
        raise ValidationError(
            self._custom_message or f"Expected date, got {type(value).__name__}"
        )

class ObjectValidator(Validator, Generic[T]):
    """
    Validator for dictionary/object values with nested field validation.
    """
    
    def __init__(self, schema: Dict[str, Validator]) -> None:
        """
        Initialize object validator with a schema defining field validators.
        
        Args:
            schema: Dictionary mapping field names to their validators
        """
        super().__init__()
        self.schema: Dict[str, Validator] = schema  # Field name -> validator mapping
        self._strict: bool = True  # Whether to reject extra fields
        self._allow_extra: bool = False  # Whether to allow fields not in schema
    
    def strict(self, strict: bool = True) -> Self:
        """
        Set strict mode for object validation.
        
        Args:
            strict: If True, reject fields not in schema
            
        Returns:
            Self for method chaining
        """
        self._strict = strict
        return self
    
    def allow_extra(self, allow: bool = True) -> Self:
        """
        Allow extra fields not defined in the schema.
        
        Args:
            allow: If True, allow extra fields
            
        Returns:
            Self for method chaining
        """
        self._allow_extra = allow
        return self
    
    def validate(self, value: Any) -> Dict[str, Any]:
        """
        Validate that the value is a dictionary with valid field values.
        
        Args:
            value: The value to validate
            
        Returns:
            Dictionary with validated field values
            
        Raises:
            ValidationError: If validation fails (wrong type, missing fields, or field validation fails)
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        # Check if value is a dictionary
        if not isinstance(value, dict):
            raise ValidationError(
                self._custom_message or f"Expected object, got {type(value).__name__}"
            )
        
        # Check for extra fields in strict mode
        if self._strict and not self._allow_extra:
            extra_fields = set(value.keys()) - set(self.schema.keys())
            if extra_fields:
                raise ValidationError(
                    f"Unexpected fields: {', '.join(extra_fields)}"
                )
        
        # Validate each field in the schema
        result: Dict[str, Any] = {}
        for field_name, validator in self.schema.items():
            if field_name in value:
                # Field exists, validate it
                try:
                    result[field_name] = validator.validate(value[field_name])
                except Exception as e:
                    # Add field context to error
                    raise ValidationError(f"{field_name}: {e}")
            elif hasattr(validator, '_optional') and validator._optional:
                # Field is optional and missing, set to None
                result[field_name] = None
            else:
                # Required field is missing
                raise ValidationError(f"Missing required field: {field_name}")
        
        return result

class ArrayValidator(Validator, Generic[T]):
    """
    Validator for list/array values with item validation and constraints.
    """
    
    def __init__(self, item_validator: Validator) -> None:
        """
        Initialize array validator with an item validator.
        
        Args:
            item_validator: Validator to apply to each item in the array
        """
        super().__init__()
        self.item_validator: Validator = item_validator  # Validator for array items
        self._min_length: Optional[int] = None  # Minimum array length
        self._max_length: Optional[int] = None  # Maximum array length
        self._unique: bool = False  # Whether items must be unique
    
    def min_length(self, length: int) -> Self:
        """
        Set the minimum length requirement for arrays.
        
        Args:
            length: Minimum number of items required
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If length is negative
        """
        if length < 0:
            raise ValueError("Minimum length must be non-negative")
        self._min_length = length
        return self
    
    def max_length(self, length: int) -> Self:
        """
        Set the maximum length requirement for arrays.
        
        Args:
            length: Maximum number of items allowed
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If length is negative
        """
        if length < 0:
            raise ValueError("Maximum length must be non-negative")
        self._max_length = length
        return self
    
    def unique(self, unique: bool = True) -> Self:
        """
        Require that all items in the array are unique.
        
        Args:
            unique: If True, require unique items
            
        Returns:
            Self for method chaining
        """
        self._unique = unique
        return self
    
    def validate(self, value: Any) -> List[T]:
        """
        Validate that the value is a list with valid items meeting all constraints.
        
        Args:
            value: The value to validate
            
        Returns:
            List with validated items
            
        Raises:
            ValidationError: If validation fails (wrong type, length, uniqueness, or item validation)
        """
        # Handle optional None values
        if self._is_optional_and_none(value):
            return value
        
        # Check if value is a list
        if not isinstance(value, list):
            raise ValidationError(
                self._custom_message or f"Expected array, got {type(value).__name__}"
            )
        
        # Check minimum length constraint
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError(
                self._custom_message or f"Array must have at least {self._min_length} items"
            )
        
        # Check maximum length constraint
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError(
                self._custom_message or f"Array must have at most {self._max_length} items"
            )
        
        # Validate each item in the array
        result: List[T] = []
        for i, item in enumerate(value):
            try:
                validated_item = self.item_validator.validate(item)
                result.append(validated_item)
            except Exception as e:
                # Add array index context to error
                raise ValidationError(f"[{i}]: {e}")
        
        # Check uniqueness constraint
        if self._unique:
            unique_items = set()
            for item in result:
                if isinstance(item, (dict, list)):
                    # For complex types, use string representation for comparison
                    item_str = str(item)
                else:
                    item_str = str(item)
                
                if item_str in unique_items:
                    raise ValidationError("Array items must be unique")
                unique_items.add(item_str)
        
        return result 