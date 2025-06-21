# Schema Builder
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
import re
from datetime import datetime

T = TypeVar('T')

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class Validator:
    """Base validator class"""
    def __init__(self):
        self.custom_message = None
    
    def with_message(self, message: str) -> 'Validator':
        """Set a custom error message"""
        self.custom_message = message
        return self
    
    def validate(self, value: Any) -> Any:
        """Base validation method - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement validate method")

class StringValidator(Validator):
    """Validator for string values"""
    def __init__(self):
        super().__init__()
        self._min_length = None
        self._max_length = None
        self._pattern = None
    
    def min_length(self, length: int) -> 'StringValidator':
        """Set minimum length requirement"""
        self._min_length = length
        return self
    
    def max_length(self, length: int) -> 'StringValidator':
        """Set maximum length requirement"""
        self._max_length = length
        return self
    
    def pattern(self, regex: str) -> 'StringValidator':
        """Set pattern requirement"""
        self._pattern = regex
        return self
    
    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValidationError(self.custom_message or f"Expected string, got {type(value).__name__}")
        
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError(self.custom_message or f"String must be at least {self._min_length} characters long")
        
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError(self.custom_message or f"String must be at most {self._max_length} characters long")
        
        if self._pattern is not None and not re.match(self._pattern, value):
            raise ValidationError(self.custom_message or f"String does not match pattern {self._pattern}")
        
        return value

class NumberValidator(Validator):
    """Validator for numeric values"""
    def __init__(self):
        super().__init__()
        self._min_value = None
        self._max_value = None
        self._optional = False
    
    def min_value(self, value: Union[int, float]) -> 'NumberValidator':
        """Set minimum value requirement"""
        self._min_value = value
        return self
    
    def max_value(self, value: Union[int, float]) -> 'NumberValidator':
        """Set maximum value requirement"""
        self._max_value = value
        return self
    
    def optional(self) -> 'NumberValidator':
        """Mark field as optional"""
        self._optional = True
        return self
    
    def validate(self, value: Any) -> Union[int, float]:
        if value is None and self._optional:
            return value
        
        if not isinstance(value, (int, float)):
            raise ValidationError(self.custom_message or f"Expected number, got {type(value).__name__}")
        
        if self._min_value is not None and value < self._min_value:
            raise ValidationError(self.custom_message or f"Value must be at least {self._min_value}")
        
        if self._max_value is not None and value > self._max_value:
            raise ValidationError(self.custom_message or f"Value must be at most {self._max_value}")
        
        return value

class BooleanValidator(Validator):
    """Validator for boolean values"""
    def validate(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise ValidationError(self.custom_message or f"Expected boolean, got {type(value).__name__}")
        return value

class DateValidator(Validator):
    """Validator for date values"""
    def validate(self, value: Any) -> datetime:
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValidationError(self.custom_message or "Invalid date format")
        elif isinstance(value, datetime):
            return value
        else:
            raise ValidationError(self.custom_message or f"Expected date, got {type(value).__name__}")

class ObjectValidator(Validator, Generic[T]):
    """Validator for object values"""
    def __init__(self, schema: Dict[str, Validator]):
        super().__init__()
        self.schema = schema
        self._optional = False
    
    def optional(self) -> 'ObjectValidator[T]':
        """Mark field as optional"""
        self._optional = True
        return self
    
    def validate(self, value: Any) -> Dict[str, Any]:
        if value is None and self._optional:
            return value
        
        if not isinstance(value, dict):
            raise ValidationError(self.custom_message or f"Expected object, got {type(value).__name__}")
        
        result = {}
        for field_name, validator in self.schema.items():
            if field_name in value:
                try:
                    result[field_name] = validator.validate(value[field_name])
                except ValidationError as e:
                    e.field = field_name
                    raise e
            elif hasattr(validator, '_optional') and validator._optional:
                result[field_name] = None
            else:
                raise ValidationError(f"Missing required field: {field_name}")
        
        return result

class ArrayValidator(Validator, Generic[T]):
    """Validator for array values"""
    def __init__(self, item_validator: Validator):
        super().__init__()
        self.item_validator = item_validator
    
    def validate(self, value: Any) -> List[T]:
        if not isinstance(value, list):
            raise ValidationError(self.custom_message or f"Expected array, got {type(value).__name__}")
        
        result = []
        for i, item in enumerate(value):
            try:
                validated_item = self.item_validator.validate(item)
                result.append(validated_item)
            except ValidationError as e:
                e.field = f"[{i}]"
                raise e
        
        return result

class Schema:
    """Main schema builder class"""
    @staticmethod
    def string() -> StringValidator:
        return StringValidator()
    
    @staticmethod
    def number() -> NumberValidator:
        return NumberValidator()
    
    @staticmethod
    def boolean() -> BooleanValidator:
        return BooleanValidator()
    
    @staticmethod
    def date() -> DateValidator:
        return DateValidator()
    
    @staticmethod
    def object(schema: Dict[str, Validator]) -> ObjectValidator:
        return ObjectValidator(schema)
    
    @staticmethod
    def array(item_validator: Validator) -> ArrayValidator:
        return ArrayValidator(item_validator)


# Example usage
if __name__ == "__main__":
    # Define a complex schema
    address_schema = Schema.object({
        'street': Schema.string(),
        'city': Schema.string(),
        'postalCode': Schema.string().pattern(r'^\d{5}$').with_message('Postal code must be 5 digits'),
        'country': Schema.string()
    })
    
    user_schema = Schema.object({
        'id': Schema.string().with_message('ID must be a string'),
        'name': Schema.string().min_length(2).max_length(50),
        'email': Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
        'age': Schema.number().optional(),
        'isActive': Schema.boolean(),
        'tags': Schema.array(Schema.string()),
        'address': address_schema.optional(),
        'metadata': Schema.object({}).optional()
    })
    
    # Validate data
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
        }
    }
    
    try:
        result = user_schema.validate(user_data)
        print("Validation successful!")
        print(f"Validated data: {result}")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        if e.field:
            print(f"Field: {e.field}") 