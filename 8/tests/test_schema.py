#!/usr/bin/env python3
"""
Comprehensive tests for the type-safe validation library
"""

import pytest
from datetime import datetime
from schema import (
    Schema, ValidationError, StringValidator, NumberValidator, 
    BooleanValidator, DateValidator, ObjectValidator, ArrayValidator
)

class TestStringValidator:
    """Test string validation with type safety"""
    
    def test_basic_string_validation(self):
        validator = Schema.string()
        assert validator.validate("hello") == "hello"
        
        with pytest.raises(ValidationError, match="Expected string"):
            validator.validate(123)
    
    def test_string_length_constraints(self):
        validator = Schema.string().min_length(3).max_length(10)
        
        # Valid cases
        assert validator.validate("hello") == "hello"
        
        # Invalid cases
        with pytest.raises(ValidationError, match="at least 3"):
            validator.validate("ab")
        
        with pytest.raises(ValidationError, match="at most 10"):
            validator.validate("this is too long")
    
    def test_string_pattern_validation(self):
        validator = Schema.string().pattern(r'^\d{3}-\d{2}-\d{4}$')
        
        # Valid case
        assert validator.validate("123-45-6789") == "123-45-6789"
        
        # Invalid case
        with pytest.raises(ValidationError, match="does not match pattern"):
            validator.validate("123-456-789")
    
    def test_string_optional(self):
        validator = Schema.string().optional()
        
        assert validator.validate(None) is None
        assert validator.validate("hello") == "hello"
        
        with pytest.raises(ValidationError, match="Expected string"):
            validator.validate(123)

class TestNumberValidator:
    """Test number validation with type safety"""
    
    def test_basic_number_validation(self):
        validator = Schema.number()
        
        assert validator.validate(42) == 42
        assert validator.validate(3.14) == 3.14
        
        with pytest.raises(ValidationError, match="Expected number"):
            validator.validate("42")
    
    def test_number_range_validation(self):
        validator = Schema.number().min_value(0).max_value(100)
        
        assert validator.validate(50) == 50
        assert validator.validate(0) == 0
        assert validator.validate(100) == 100
        
        with pytest.raises(ValidationError, match="at least 0"):
            validator.validate(-1)
        
        with pytest.raises(ValidationError, match="at most 100"):
            validator.validate(101)
    
    def test_integer_only_validation(self):
        validator = Schema.number().integer_only()
        
        assert validator.validate(42) == 42
        
        with pytest.raises(ValidationError, match="Expected integer"):
            validator.validate(3.14)
    
    def test_number_optional(self):
        validator = Schema.number().optional()
        
        assert validator.validate(None) is None
        assert validator.validate(42) == 42

class TestBooleanValidator:
    """Test boolean validation with type safety"""
    
    def test_strict_boolean_validation(self):
        validator = Schema.boolean().strict()
        
        assert validator.validate(True) is True
        assert validator.validate(False) is False
        
        with pytest.raises(ValidationError, match="Expected boolean"):
            validator.validate(1)
    
    def test_non_strict_boolean_validation(self):
        validator = Schema.boolean().strict(False)
        
        assert validator.validate(True) is True
        assert validator.validate(False) is False
        assert validator.validate(1) is True
        assert validator.validate(0) is False
        assert validator.validate("hello") is True
        assert validator.validate("") is False

class TestDateValidator:
    """Test date validation with type safety"""
    
    def test_iso_date_validation(self):
        validator = Schema.date()
        
        # Valid ISO format
        date_str = "2024-01-01T12:00:00"
        result = validator.validate(date_str)
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1
    
    def test_datetime_object_validation(self):
        validator = Schema.date()
        dt = datetime(2024, 1, 1, 12, 0, 0)
        
        result = validator.validate(dt)
        assert result == dt
    
    def test_timestamp_validation(self):
        validator = Schema.date().formats('timestamp')
        
        timestamp = 1704110400  # 2024-01-01 12:00:00 UTC
        result = validator.validate(timestamp)
        assert isinstance(result, datetime)

class TestArrayValidator:
    """Test array validation with type safety"""
    
    def test_basic_array_validation(self):
        validator = Schema.array(Schema.string())
        
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]
        
        with pytest.raises(ValidationError, match="Expected array"):
            validator.validate("not an array")
    
    def test_array_length_constraints(self):
        validator = Schema.array(Schema.string()).min_length(2).max_length(4)
        
        assert validator.validate(["a", "b"]) == ["a", "b"]
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]
        
        with pytest.raises(ValidationError, match="at least 2"):
            validator.validate(["a"])
        
        with pytest.raises(ValidationError, match="at most 4"):
            validator.validate(["a", "b", "c", "d", "e"])
    
    def test_array_unique_items(self):
        validator = Schema.array(Schema.string()).unique()
        
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]
        
        with pytest.raises(ValidationError, match="must be unique"):
            validator.validate(["a", "b", "a"])
    
    def test_nested_array_validation(self):
        inner_validator = Schema.array(Schema.number())
        outer_validator = Schema.array(inner_validator)
        
        data = [[1, 2], [3, 4, 5]]
        result = outer_validator.validate(data)
        assert result == [[1, 2], [3, 4, 5]]

class TestObjectValidator:
    """Test object validation with type safety"""
    
    def test_basic_object_validation(self):
        schema = {
            'name': Schema.string(),
            'age': Schema.number()
        }
        validator = Schema.object(schema)
        
        data = {'name': 'John', 'age': 30}
        result = validator.validate(data)
        assert result == data
    
    def test_missing_required_fields(self):
        schema = {
            'name': Schema.string(),
            'age': Schema.number()
        }
        validator = Schema.object(schema)
        
        with pytest.raises(ValidationError, match="Missing required field"):
            validator.validate({'name': 'John'})
    
    def test_optional_fields(self):
        schema = {
            'name': Schema.string(),
            'age': Schema.number().optional()
        }
        validator = Schema.object(schema)
        
        data = {'name': 'John'}
        result = validator.validate(data)
        assert result['name'] == 'John'
        assert result['age'] is None
    
    def test_strict_object_validation(self):
        schema = {'name': Schema.string()}
        validator = Schema.object(schema).strict()
        
        with pytest.raises(ValidationError, match="Unexpected fields"):
            validator.validate({'name': 'John', 'extra': 'field'})
    
    def test_allow_extra_fields(self):
        schema = {'name': Schema.string()}
        validator = Schema.object(schema).allow_extra()
        
        data = {'name': 'John', 'extra': 'field'}
        result = validator.validate(data)
        assert result['name'] == 'John'
        # Extra field is not included in result

class TestComplexNestedValidation:
    """Test complex nested validation scenarios"""
    
    def test_deeply_nested_objects(self):
        address_schema = Schema.object({
            'street': Schema.string().min_length(1),
            'city': Schema.string().min_length(1),
            'country': Schema.string().min_length(2)
        })
        
        user_schema = Schema.object({
            'id': Schema.string().min_length(1),
            'name': Schema.string().min_length(2),
            'addresses': Schema.array(address_schema).min_length(1)
        })
        
        data = {
            'id': '123',
            'name': 'John Doe',
            'addresses': [
                {'street': '123 Main St', 'city': 'Anytown', 'country': 'USA'},
                {'street': '456 Oak Ave', 'city': 'Somewhere', 'country': 'Canada'}
            ]
        }
        
        result = user_schema.validate(data)
        assert len(result['addresses']) == 2
        assert result['addresses'][0]['street'] == '123 Main St'
    
    def test_validation_error_paths(self):
        address_schema = Schema.object({
            'street': Schema.string().min_length(1),
            'city': Schema.string().min_length(1)
        })
        
        user_schema = Schema.object({
            'name': Schema.string().min_length(2),
            'addresses': Schema.array(address_schema)
        })
        
        data = {
            'name': 'John',
            'addresses': [
                {'street': '', 'city': 'Anytown'},  # Invalid: empty street
                {'street': '123 Main St', 'city': 'Anytown'}  # Valid
            ]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            user_schema.validate(data)
        
        # Check that the error path includes the array index
        assert "addresses" in str(exc_info.value)
        assert "[0]" in str(exc_info.value)

class TestTypeSafety:
    """Test type safety features"""
    
    def test_method_chaining_type_safety(self):
        # This should work without type errors
        validator = (
            Schema.string()
            .min_length(1)
            .max_length(100)
            .pattern(r'^[a-zA-Z]+$')
            .with_message("Custom error")
        )
        
        assert isinstance(validator, StringValidator)
    
    def test_generic_type_safety(self):
        # Test that generic types work correctly
        string_array_validator = Schema.array(Schema.string())
        number_array_validator = Schema.array(Schema.number())
        
        # These should have different inferred types
        assert string_array_validator.validate(["a", "b"]) == ["a", "b"]
        assert number_array_validator.validate([1, 2]) == [1, 2]

if __name__ == "__main__":
    # Run basic tests
    print("Running validation library tests...")
    
    # Test basic functionality
    string_validator = Schema.string().min_length(1).max_length(10)
    assert string_validator.validate("hello") == "hello"
    
    number_validator = Schema.number().min_value(0).max_value(100)
    assert number_validator.validate(50) == 50
    
    boolean_validator = Schema.boolean()
    assert boolean_validator.validate(True) is True
    
    print("✅ All basic tests passed!")
    
    # Test complex validation
    user_schema = Schema.object({
        'name': Schema.string().min_length(2),
        'age': Schema.number().min_value(0).optional(),
        'tags': Schema.array(Schema.string()).unique()
    })
    
    data = {
        'name': 'John Doe',
        'age': 30,
        'tags': ['developer', 'designer']
    }
    
    result = user_schema.validate(data)
    print(f"✅ Complex validation passed: {result}") 