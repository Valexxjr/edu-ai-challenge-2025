#!/usr/bin/env python3
"""
Test script to check OpenAI API access and available models
"""

import os
import openai

def test_openai_access():
    """Test OpenAI API access and list available models."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("No OPENAI_API_KEY found in environment")
        return
    
    print(f"API Key found: {api_key[:10]}...")
    
    # Set the API key
    openai.api_key = api_key
    
    try:
        # Try to list models
        print("Attempting to list available models...")
        models = openai.models.list()
        print(f"Success! Found {len(models.data)} models:")
        for model in models.data[:10]:  # Show first 10
            print(f"  - {model.id}")
        
        # Try a simple completion with a basic model
        print("\nTesting simple completion...")
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=10
            )
            print(f"Success! Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"Chat completion failed: {e}")
            
    except Exception as e:
        print(f"Error accessing OpenAI API: {e}")
        print("\nPossible issues:")
        print("1. Your API key might be for a different service")
        print("2. You might need to upgrade your OpenAI plan")
        print("3. Your organization might have restrictions")
        print("4. You might be using a custom endpoint")

if __name__ == "__main__":
    test_openai_access() 