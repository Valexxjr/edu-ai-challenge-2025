#!/usr/bin/env python3
"""
Comprehensive tests for the type-safe validation library
This test suite covers all validator types and their functionality
"""

import pytest
import sys
import os
from datetime import datetime

# Add the parent directory to the path so we can import the schema package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schema import (
    Schema, ValidationError, StringValidator, NumberValidator, 
    BooleanValidator, DateValidator, ObjectValidator, ArrayValidator
)

class TestStringValidator:
    """Test string validation with type safety"""
    
    def test_basic_string_validation(self):
        """Test basic string type validation - accepts strings, rejects non-strings"""
        validator = Schema.string()
        assert validator.validate("hello") == "hello"  # Valid string should pass
        
        with pytest.raises(ValidationError, match="Expected string"):
            validator.validate(123)  # Non-string should fail
    
    def test_string_length_constraints(self):
        """Test string length validation with min and max constraints"""
        validator = Schema.string().min_length(3).max_length(10)
        
        # Valid cases - strings within length bounds
        assert validator.validate("hello") == "hello"
        
        # Invalid cases - strings outside length bounds
        with pytest.raises(ValidationError, match="at least 3"):
            validator.validate("ab")  # Too short
        
        with pytest.raises(ValidationError, match="at most 10"):
            validator.validate("this is too long")  # Too long
    
    def test_string_pattern_validation(self):
        """Test string pattern validation using regex"""
        validator = Schema.string().pattern(r'^\d{3}-\d{2}-\d{4}$')  # SSN format
        
        # Valid case - matches pattern
        assert validator.validate("123-45-6789") == "123-45-6789"
        
        # Invalid case - doesn't match pattern
        with pytest.raises(ValidationError, match="does not match pattern"):
            validator.validate("123-456-789")
    
    def test_string_optional(self):
        """Test optional string validation - allows None values"""
        validator = Schema.string().optional()
        
        assert validator.validate(None) is None  # None should be allowed
        assert validator.validate("hello") == "hello"  # Valid string should still work
        
        with pytest.raises(ValidationError, match="Expected string"):
            validator.validate(123)  # Non-string should still fail

class TestNumberValidator:
    """Test number validation with type safety"""
    
    def test_basic_number_validation(self):
        """Test basic number type validation - accepts int/float, rejects non-numbers"""
        validator = Schema.number()
        
        assert validator.validate(42) == 42  # Integer should pass
        assert validator.validate(3.14) == 3.14  # Float should pass
        
        with pytest.raises(ValidationError, match="Expected number"):
            validator.validate("42")  # String should fail
    
    def test_number_range_validation(self):
        """Test number range validation with min and max constraints"""
        validator = Schema.number().min_value(0).max_value(100)
        
        assert validator.validate(50) == 50  # Within range
        assert validator.validate(0) == 0    # At minimum
        assert validator.validate(100) == 100  # At maximum
        
        with pytest.raises(ValidationError, match="at least 0"):
            validator.validate(-1)  # Below minimum
        
        with pytest.raises(ValidationError, match="at most 100"):
            validator.validate(101)  # Above maximum
    
    def test_integer_only_validation(self):
        """Test integer-only validation - rejects floats"""
        validator = Schema.number().integer_only()
        
        assert validator.validate(42) == 42  # Integer should pass
        
        with pytest.raises(ValidationError, match="Expected integer"):
            validator.validate(3.14)  # Float should fail
    
    def test_number_optional(self):
        """Test optional number validation - allows None values"""
        validator = Schema.number().optional()
        
        assert validator.validate(None) is None  # None should be allowed
        assert validator.validate(42) == 42  # Valid number should still work

class TestBooleanValidator:
    """Test boolean validation with type safety"""
    
    def test_strict_boolean_validation(self):
        """Test strict boolean validation - only accepts True/False"""
        validator = Schema.boolean().strict()
        
        assert validator.validate(True) is True   # True should pass
        assert validator.validate(False) is False  # False should pass
        
        with pytest.raises(ValidationError, match="Expected boolean"):
            validator.validate(1)  # Non-boolean should fail
    
    def test_non_strict_boolean_validation(self):
        """Test non-strict boolean validation - accepts truthy/falsy values"""
        validator = Schema.boolean().strict(False)
        
        assert validator.validate(True) is True   # True should pass
        assert validator.validate(False) is False  # False should pass
        assert validator.validate(1) is True      # Truthy should become True
        assert validator.validate(0) is False     # Falsy should become False
        assert validator.validate("hello") is True  # Non-empty string is truthy
        assert validator.validate("") is False    # Empty string is falsy

class TestDateValidator:
    """Test date validation with type safety"""
    
    def test_iso_date_validation(self):
        """Test ISO date string validation"""
        validator = Schema.date()
        
        # Valid ISO format string
        date_str = "2024-01-01T12:00:00"
        result = validator.validate(date_str)
        assert isinstance(result, datetime)  # Should return datetime object
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1
    
    def test_datetime_object_validation(self):
        """Test datetime object validation - should pass through unchanged"""
        validator = Schema.date()
        dt = datetime(2024, 1, 1, 12, 0, 0)
        
        result = validator.validate(dt)
        assert result == dt  # Should return same datetime object
    
    def test_timestamp_validation(self):
        """Test timestamp validation - converts numeric timestamp to datetime"""
        validator = Schema.date().formats('timestamp')
        
        timestamp = 1704110400  # Unix timestamp for 2024-01-01 12:00:00 UTC
        result = validator.validate(timestamp)
        assert isinstance(result, datetime)  # Should return datetime object

class TestArrayValidator:
    """Test array validation with type safety"""
    
    def test_basic_array_validation(self):
        """Test basic array type validation - accepts lists, rejects non-lists"""
        validator = Schema.array(Schema.string())
        
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]  # Valid list should pass
        
        with pytest.raises(ValidationError, match="Expected array"):
            validator.validate("not an array")  # Non-list should fail
    
    def test_array_length_constraints(self):
        """Test array length validation with min and max constraints"""
        validator = Schema.array(Schema.string()).min_length(2).max_length(4)
        
        assert validator.validate(["a", "b"]) == ["a", "b"]      # At minimum length
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]  # Within range
        
        with pytest.raises(ValidationError, match="at least 2"):
            validator.validate(["a"])  # Too few items
        
        with pytest.raises(ValidationError, match="at most 4"):
            validator.validate(["a", "b", "c", "d", "e"])  # Too many items
    
    def test_array_unique_items(self):
        """Test array uniqueness validation - requires all items to be unique"""
        validator = Schema.array(Schema.string()).unique()
        
        assert validator.validate(["a", "b", "c"]) == ["a", "b", "c"]  # Unique items should pass
        
        with pytest.raises(ValidationError, match="must be unique"):
            validator.validate(["a", "b", "a"])  # Duplicate items should fail
    
    def test_nested_array_validation(self):
        """Test nested array validation - arrays of arrays"""
        inner_validator = Schema.array(Schema.number())  # Array of numbers
        outer_validator = Schema.array(inner_validator)   # Array of arrays
        
        data = [[1, 2], [3, 4, 5]]  # Valid nested structure
        result = outer_validator.validate(data)
        assert result == [[1, 2], [3, 4, 5]]

class TestObjectValidator:
    """Test object validation with type safety"""
    
    def test_basic_object_validation(self):
        """Test basic object validation with required fields"""
        schema = {
            'name': Schema.string(),
            'age': Schema.number()
        }
        validator = Schema.object(schema)
        
        data = {'name': 'John', 'age': 30}  # Valid object with all required fields
        result = validator.validate(data)
        assert result == data
    
    def test_missing_required_fields(self):
        """Test object validation with missing required fields"""
        schema = {
            'name': Schema.string(),
            'age': Schema.number()
        }
        validator = Schema.object(schema)
        
        with pytest.raises(ValidationError, match="Missing required field"):
            validator.validate({'name': 'John'})  # Missing 'age' field should fail
    
    def test_optional_fields(self):
        """Test object validation with optional fields"""
        schema = {
            'name': Schema.string(),
            'age': Schema.number().optional()  # Age is optional
        }
        validator = Schema.object(schema)
        
        data = {'name': 'John'}  # Missing optional field should be OK
        result = validator.validate(data)
        assert result['name'] == 'John'
        assert result['age'] is None  # Optional field should be set to None
    
    def test_strict_object_validation(self):
        """Test strict object validation - rejects extra fields"""
        schema = {'name': Schema.string()}
        validator = Schema.object(schema).strict()
        
        with pytest.raises(ValidationError, match="Unexpected fields"):
            validator.validate({'name': 'John', 'extra': 'field'})  # Extra field should fail
    
    def test_allow_extra_fields(self):
        """Test object validation that allows extra fields"""
        schema = {'name': Schema.string()}
        validator = Schema.object(schema).allow_extra()
        
        data = {'name': 'John', 'extra': 'field'}  # Extra field should be allowed
        result = validator.validate(data)
        assert result['name'] == 'John'  # Only schema fields are included in result

class TestComplexNestedValidation:
    """Test complex nested validation scenarios"""
    
    def test_deeply_nested_objects(self):
        """Test validation of deeply nested object structures"""
        # Define nested schemas
        address_schema = Schema.object({
            'street': Schema.string().min_length(1),
            'city': Schema.string().min_length(1),
            'country': Schema.string().min_length(2)
        })
        
        user_schema = Schema.object({
            'id': Schema.string().min_length(1),
            'name': Schema.string().min_length(2),
            'addresses': Schema.array(address_schema).min_length(1)  # Array of addresses
        })
        
        # Valid nested data
        data = {
            'id': '123',
            'name': 'John Doe',
            'addresses': [
                {'street': '123 Main St', 'city': 'Anytown', 'country': 'USA'},
                {'street': '456 Oak Ave', 'city': 'Somewhere', 'country': 'Canada'}
            ]
        }
        
        result = user_schema.validate(data)
        assert len(result['addresses']) == 2  # Should have 2 addresses
        assert result['addresses'][0]['street'] == '123 Main St'  # Nested validation should work
    
    def test_validation_error_paths(self):
        """Test that validation errors include proper field paths for nested structures"""
        address_schema = Schema.object({
            'street': Schema.string().min_length(1),
            'city': Schema.string().min_length(1)
        })
        
        user_schema = Schema.object({
            'name': Schema.string().min_length(2),
            'addresses': Schema.array(address_schema)
        })
        
        # Data with validation error in nested structure
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
        assert "addresses" in str(exc_info.value)  # Should mention addresses field
        assert "[0]" in str(exc_info.value)  # Should mention array index

class TestTypeSafety:
    """Test type safety features of the validation library"""
    
    def test_method_chaining_type_safety(self):
        """Test that method chaining works correctly with proper type safety"""
        # This should work without type errors - method chaining returns correct types
        validator = (
            Schema.string()
            .min_length(1)
            .max_length(100)
            .pattern(r'^[a-zA-Z]+$')
            .with_message("Custom error")
        )
        
        assert isinstance(validator, StringValidator)  # Should be correct type
    
    def test_generic_type_safety(self):
        """Test that generic types work correctly for different validator types"""
        # Test that generic types work correctly
        string_array_validator = Schema.array(Schema.string())  # Array of strings
        number_array_validator = Schema.array(Schema.number())  # Array of numbers
        
        # These should have different inferred types and work correctly
        assert string_array_validator.validate(["a", "b"]) == ["a", "b"]  # String array
        assert number_array_validator.validate([1, 2]) == [1, 2]  # Number array

if __name__ == "__main__":
    # Run basic tests when script is executed directly
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