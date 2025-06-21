# Type-Safe Validation Library

A robust, type-safe validation library for Python that can validate complex data structures with comprehensive error reporting and type checking.

## Features

### ✅ Type Safety
- **Full Type Hints**: All validators use proper Python type annotations
- **Generic Types**: Support for generic validation with `TypeVar`
- **Protocol Classes**: Runtime-checkable validator protocols
- **Self References**: Proper `Self` type annotations for method chaining

### ✅ Primitive Type Validators
- **StringValidator**: Length constraints, regex patterns, custom messages
- **NumberValidator**: Range validation, integer-only mode, optional fields
- **BooleanValidator**: Strict mode (True/False only) or truthy/falsy
- **DateValidator**: Multiple format support (ISO, timestamps, custom formats)

### ✅ Complex Type Validators
- **ObjectValidator**: Nested object validation with field requirements
- **ArrayValidator**: Item validation, length constraints, uniqueness
- **Nested Validation**: Deep validation with error path tracking

### ✅ Advanced Features
- **Method Chaining**: Fluent API for building complex validators
- **Custom Error Messages**: Contextual error messages for better UX
- **Optional Fields**: Support for nullable/optional data
- **Error Path Tracking**: Detailed error paths for nested validation
- **Strict Mode**: Configurable strictness for objects and booleans

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from schema import Schema

# Define a simple schema
user_schema = Schema.object({
    'name': Schema.string().min_length(2).max_length(50),
    'email': Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
    'age': Schema.number().min_value(0).max_value(150).optional(),
    'is_active': Schema.boolean()
})

# Validate data
try:
    result = user_schema.validate({
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30,
        'is_active': True
    })
    print("✅ Validation successful!")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
```

## Validator Types

### StringValidator

```python
# Basic string validation
validator = Schema.string()

# With constraints
validator = (
    Schema.string()
    .min_length(3)
    .max_length(100)
    .pattern(r'^[a-zA-Z\s]+$')
    .with_message("Name must contain only letters and spaces")
)
```

**Features:**
- `min_length(length)`: Minimum string length
- `max_length(length)`: Maximum string length  
- `pattern(regex)`: Regex pattern validation
- `with_message(message)`: Custom error message
- `optional()`: Allow None values

### NumberValidator

```python
# Basic number validation
validator = Schema.number()

# With constraints
validator = (
    Schema.number()
    .min_value(0)
    .max_value(100)
    .integer_only()
    .optional()
)
```

**Features:**
- `min_value(value)`: Minimum numeric value
- `max_value(value)`: Maximum numeric value
- `integer_only()`: Restrict to integers only
- `optional()`: Allow None values

### BooleanValidator

```python
# Strict boolean (True/False only)
validator = Schema.boolean().strict()

# Non-strict (truthy/falsy values)
validator = Schema.boolean().strict(False)
```

**Features:**
- `strict(strict=True)`: Only accept True/False vs truthy/falsy
- `optional()`: Allow None values

### DateValidator

```python
# ISO format dates
validator = Schema.date()

# Multiple formats
validator = Schema.date().formats('iso', '%Y-%m-%d', 'timestamp')
```

**Features:**
- `formats(*formats)`: Specify accepted date formats
- Supports ISO strings, datetime objects, timestamps
- `optional()`: Allow None values

### ArrayValidator

```python
# Array of strings
validator = Schema.array(Schema.string())

# With constraints
validator = (
    Schema.array(Schema.number())
    .min_length(1)
    .max_length(10)
    .unique()
)
```

**Features:**
- `min_length(length)`: Minimum array length
- `max_length(length)`: Maximum array length
- `unique()`: Require unique items
- Nested validation for array items

### ObjectValidator

```python
# Simple object
validator = Schema.object({
    'name': Schema.string(),
    'age': Schema.number()
})

# With options
validator = (
    Schema.object({
        'name': Schema.string(),
        'age': Schema.number()
    })
    .strict()  # Reject extra fields
    .allow_extra()  # Allow extra fields
)
```

**Features:**
- `strict(strict=True)`: Reject fields not in schema
- `allow_extra(allow=True)`: Allow extra fields
- Nested validation for object fields
- `optional()`: Allow None values

## Complex Examples

### Nested Object Validation

```python
# Address schema
address_schema = Schema.object({
    'street': Schema.string().min_length(1),
    'city': Schema.string().min_length(1),
    'postal_code': Schema.string().pattern(r'^\d{5}$'),
    'country': Schema.string().min_length(2)
})

# User schema with nested address
user_schema = Schema.object({
    'id': Schema.string().min_length(1),
    'name': Schema.string().min_length(2).max_length(50),
    'email': Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
    'addresses': Schema.array(address_schema).min_length(1),
    'metadata': Schema.object({}).allow_extra().optional()
})
```

### Array of Objects with Constraints

```python
# Product schema
product_schema = Schema.object({
    'id': Schema.string().min_length(1),
    'name': Schema.string().min_length(1).max_length(100),
    'price': Schema.number().min_value(0),
    'tags': Schema.array(Schema.string()).unique()
})

# Order schema
order_schema = Schema.object({
    'order_id': Schema.string().pattern(r'^ORD-\d{6}$'),
    'customer_id': Schema.string().min_length(1),
    'products': Schema.array(product_schema).min_length(1).max_length(50),
    'total': Schema.number().min_value(0),
    'status': Schema.string().pattern(r'^(pending|confirmed|shipped|delivered)$')
})
```

## Error Handling

The library provides detailed error information:

```python
try:
    result = schema.validate(data)
except ValidationError as e:
    print(f"Error: {e.message}")
    print(f"Path: {' -> '.join(e.path)}")
    print(f"Field: {e.field}")
```

**Error Properties:**
- `message`: Human-readable error message
- `path`: List of field names leading to the error
- `field`: The specific field that failed validation

## Type Safety Best Practices

### 1. Use Type Hints

```python
from typing import Dict, List, Any

def validate_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    schema = Schema.object({
        'name': Schema.string(),
        'age': Schema.number()
    })
    return schema.validate(data)
```

### 2. Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class UserValidator(Generic[T]):
    def __init__(self, schema: ObjectValidator[T]):
        self.schema = schema
    
    def validate(self, data: Any) -> T:
        return self.schema.validate(data)
```

### 3. Protocol Classes

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class ValidatorProtocol(Protocol):
    def validate(self, value: Any) -> Any: ...
    def with_message(self, message: str) -> Self: ...

def accepts_validator(validator: ValidatorProtocol) -> None:
    # This function accepts any object that implements the protocol
    pass
```

## Testing

Run the test suite:

```bash
python test_schema.py
```

Or use pytest for more detailed testing:

```bash
pytest test_schema.py -v
```

## Performance Considerations

- **Compiled Regex**: String validators compile regex patterns once
- **Lazy Validation**: Validation only occurs when `validate()` is called
- **Efficient Path Tracking**: Error paths are built incrementally
- **Type Checking**: Minimal runtime overhead for type annotations

## Contributing

1. Follow Python type safety best practices
2. Add comprehensive tests for new features
3. Use proper type hints and documentation
4. Ensure backward compatibility

## License

MIT License - see LICENSE file for details. 