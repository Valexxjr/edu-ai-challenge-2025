# Schema Builder - Type-Safe Validation Library
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Protocol, runtime_checkable
from typing_extensions import Self
import re
from datetime import datetime
from abc import ABC, abstractmethod

# Type variables for generic validators
T = TypeVar('T')
V = TypeVar('V', bound='Validator')

@runtime_checkable
class ValidatorProtocol(Protocol):
    """Protocol for validator objects"""
    def validate(self, value: Any) -> Any: ...
    def with_message(self, message: str) -> Self: ...

class ValidationError(Exception):
    """Custom exception for validation errors with field path support"""
    def __init__(self, message: str, field: Optional[str] = None, path: Optional[List[str]] = None):
        self.message = message
        self.field = field
        self.path = path or []
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.path:
            path_str = " -> ".join(self.path)
            return f"{path_str}: {self.message}"
        return self.message

class Validator(ABC):
    """Abstract base validator class with proper type safety"""
    
    def __init__(self) -> None:
        self._custom_message: Optional[str] = None
        self._optional: bool = False
    
    def with_message(self, message: str) -> Self:
        """Set a custom error message"""
        self._custom_message = message
        return self
    
    def optional(self) -> Self:
        """Mark field as optional"""
        self._optional = True
        return self
    
    def _is_optional_and_none(self, value: Any) -> bool:
        """Check if value is None and field is optional"""
        return value is None and self._optional
    
    @abstractmethod
    def validate(self, value: Any) -> Any:
        """Abstract validation method - must be implemented by subclasses"""
        pass

class StringValidator(Validator):
    """Type-safe validator for string values"""
    
    def __init__(self) -> None:
        super().__init__()
        self._min_length: Optional[int] = None
        self._max_length: Optional[int] = None
        self._pattern: Optional[str] = None
        self._compiled_pattern: Optional[re.Pattern] = None
    
    def min_length(self, length: int) -> Self:
        """Set minimum length requirement"""
        if length < 0:
            raise ValueError("Minimum length must be non-negative")
        self._min_length = length
        return self
    
    def max_length(self, length: int) -> Self:
        """Set maximum length requirement"""
        if length < 0:
            raise ValueError("Maximum length must be non-negative")
        self._max_length = length
        return self
    
    def pattern(self, regex: str) -> Self:
        """Set pattern requirement"""
        try:
            self._pattern = regex
            self._compiled_pattern = re.compile(regex)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        return self
    
    def validate(self, value: Any) -> str:
        if self._is_optional_and_none(value):
            return value
        
        if not isinstance(value, str):
            raise ValidationError(
                self._custom_message or f"Expected string, got {type(value).__name__}"
            )
        
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError(
                self._custom_message or f"String must be at least {self._min_length} characters long"
            )
        
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError(
                self._custom_message or f"String must be at most {self._max_length} characters long"
            )
        
        if self._compiled_pattern is not None and not self._compiled_pattern.match(value):
            raise ValidationError(
                self._custom_message or f"String does not match pattern {self._pattern}"
            )
        
        return value

class NumberValidator(Validator):
    """Type-safe validator for numeric values"""
    
    def __init__(self) -> None:
        super().__init__()
        self._min_value: Optional[Union[int, float]] = None
        self._max_value: Optional[Union[int, float]] = None
        self._integer_only: bool = False
    
    def min_value(self, value: Union[int, float]) -> Self:
        """Set minimum value requirement"""
        self._min_value = value
        return self
    
    def max_value(self, value: Union[int, float]) -> Self:
        """Set maximum value requirement"""
        self._max_value = value
        return self
    
    def integer_only(self) -> Self:
        """Restrict to integer values only"""
        self._integer_only = True
        return self
    
    def validate(self, value: Any) -> Union[int, float]:
        if self._is_optional_and_none(value):
            return value
        
        if not isinstance(value, (int, float)):
            raise ValidationError(
                self._custom_message or f"Expected number, got {type(value).__name__}"
            )
        
        if self._integer_only and not isinstance(value, int):
            raise ValidationError(
                self._custom_message or "Expected integer, got float"
            )
        
        if self._min_value is not None and value < self._min_value:
            raise ValidationError(
                self._custom_message or f"Value must be at least {self._min_value}"
            )
        
        if self._max_value is not None and value > self._max_value:
            raise ValidationError(
                self._custom_message or f"Value must be at most {self._max_value}"
            )
        
        return value

class BooleanValidator(Validator):
    """Type-safe validator for boolean values"""
    
    def __init__(self) -> None:
        super().__init__()
        self._strict: bool = True
    
    def strict(self, strict: bool = True) -> Self:
        """Set strict mode (only True/False vs truthy/falsy)"""
        self._strict = strict
        return self
    
    def validate(self, value: Any) -> bool:
        if self._is_optional_and_none(value):
            return value
        
        if self._strict:
            if not isinstance(value, bool):
                raise ValidationError(
                    self._custom_message or f"Expected boolean, got {type(value).__name__}"
                )
            return value
        else:
            # Allow truthy/falsy values
            return bool(value)

class DateValidator(Validator):
    """Type-safe validator for date values"""
    
    def __init__(self) -> None:
        super().__init__()
        self._formats: List[str] = ['iso', 'timestamp']
    
    def formats(self, *formats: str) -> Self:
        """Set accepted date formats"""
        self._formats = list(formats)
        return self
    
    def validate(self, value: Any) -> datetime:
        if self._is_optional_and_none(value):
            return value
        
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            # Try ISO format
            if 'iso' in self._formats:
                try:
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            # Try other formats if specified
            for fmt in self._formats:
                if fmt != 'iso':
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
        
        elif isinstance(value, (int, float)) and 'timestamp' in self._formats:
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                pass
        
        raise ValidationError(
            self._custom_message or f"Expected date, got {type(value).__name__}"
        )

class ObjectValidator(Validator, Generic[T]):
    """Type-safe validator for object values with nested validation"""
    
    def __init__(self, schema: Dict[str, Validator]) -> None:
        super().__init__()
        self.schema: Dict[str, Validator] = schema
        self._strict: bool = True
        self._allow_extra: bool = False
    
    def strict(self, strict: bool = True) -> Self:
        """Set strict mode (reject extra fields)"""
        self._strict = strict
        return self
    
    def allow_extra(self, allow: bool = True) -> Self:
        """Allow extra fields not in schema"""
        self._allow_extra = allow
        return self
    
    def validate(self, value: Any) -> Dict[str, Any]:
        if self._is_optional_and_none(value):
            return value
        
        if not isinstance(value, dict):
            raise ValidationError(
                self._custom_message or f"Expected object, got {type(value).__name__}"
            )
        
        if self._strict and not self._allow_extra:
            extra_fields = set(value.keys()) - set(self.schema.keys())
            if extra_fields:
                raise ValidationError(
                    f"Unexpected fields: {', '.join(extra_fields)}"
                )
        
        result: Dict[str, Any] = {}
        for field_name, validator in self.schema.items():
            if field_name in value:
                try:
                    result[field_name] = validator.validate(value[field_name])
                except ValidationError as e:
                    # Add field to error path
                    e.path = e.path + [field_name]
                    raise e
            elif hasattr(validator, '_optional') and validator._optional:
                result[field_name] = None
            else:
                raise ValidationError(f"Missing required field: {field_name}")
        
        return result

class ArrayValidator(Validator, Generic[T]):
    """Type-safe validator for array values with item validation"""
    
    def __init__(self, item_validator: Validator) -> None:
        super().__init__()
        self.item_validator: Validator = item_validator
        self._min_length: Optional[int] = None
        self._max_length: Optional[int] = None
        self._unique: bool = False
    
    def min_length(self, length: int) -> Self:
        """Set minimum array length"""
        if length < 0:
            raise ValueError("Minimum length must be non-negative")
        self._min_length = length
        return self
    
    def max_length(self, length: int) -> Self:
        """Set maximum array length"""
        if length < 0:
            raise ValueError("Maximum length must be non-negative")
        self._max_length = length
        return self
    
    def unique(self, unique: bool = True) -> Self:
        """Require unique items"""
        self._unique = unique
        return self
    
    def validate(self, value: Any) -> List[T]:
        if self._is_optional_and_none(value):
            return value
        
        if not isinstance(value, list):
            raise ValidationError(
                self._custom_message or f"Expected array, got {type(value).__name__}"
            )
        
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError(
                self._custom_message or f"Array must have at least {self._min_length} items"
            )
        
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError(
                self._custom_message or f"Array must have at most {self._max_length} items"
            )
        
        result: List[T] = []
        for i, item in enumerate(value):
            try:
                validated_item = self.item_validator.validate(item)
                result.append(validated_item)
            except ValidationError as e:
                e.path = e.path + [f"[{i}]"]
                raise e
        
        if self._unique:
            unique_items = set()
            for item in result:
                if isinstance(item, (dict, list)):
                    # For complex types, use string representation
                    item_str = str(item)
                else:
                    item_str = str(item)
                
                if item_str in unique_items:
                    raise ValidationError("Array items must be unique")
                unique_items.add(item_str)
        
        return result

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
    def object(schema: Dict[str, Validator]) -> ObjectValidator:
        """Create an object validator with nested schema"""
        return ObjectValidator(schema)
    
    @staticmethod
    def array(item_validator: Validator) -> ArrayValidator:
        """Create an array validator with item validation"""
        return ArrayValidator(item_validator)


# Example usage and testing
if __name__ == "__main__":
    # Define a complex schema with enhanced type safety
    address_schema = Schema.object({
        'street': Schema.string().min_length(1).max_length(100),
        'city': Schema.string().min_length(1).max_length(50),
        'postalCode': Schema.string().pattern(r'^\d{5}$').with_message('Postal code must be 5 digits'),
        'country': Schema.string().min_length(2).max_length(50)
    })
    
    user_schema = Schema.object({
        'id': Schema.string().min_length(1).with_message('ID must be a non-empty string'),
        'name': Schema.string().min_length(2).max_length(50),
        'email': Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').with_message('Invalid email format'),
        'age': Schema.number().min_value(0).max_value(150).integer_only().optional(),
        'isActive': Schema.boolean(),
        'tags': Schema.array(Schema.string().min_length(1)).min_length(0).max_length(10).unique(),
        'address': address_schema.optional(),
        'metadata': Schema.object({}).allow_extra().optional()
    })
    
    # Test data
    user_data = {
        'id': "12345",
        'name': "John Doe",
        'email': "john@example.com",
        'isActive': True,
        'tags': ["developer", "designer"],
        'address': {
            'street': "123 Main St",
            'city': "Anytown",
            'postalCode': "12345",
            'country': "USA"
        },
        'metadata': {
            'created_at': "2024-01-01T00:00:00",
            'extra_field': "should be allowed"
        }
    }
    
    try:
        result = user_schema.validate(user_data)
        print("✅ Validation successful!")
        print(f"Validated data: {result}")
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if e.path:
            print(f"Path: {' -> '.join(e.path)}") 