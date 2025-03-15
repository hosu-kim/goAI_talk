#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test script to verify the OpenAI API key is loaded correctly.
"""

import os
from dotenv import load_dotenv
import sys

# Try to load .env file from different locations
possible_paths = [
    '.env',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"Found .env file at: {path}")
        load_dotenv(path)
        break
else:
    print("No .env file found in any of the expected locations.")

# Check if API keys are loaded
openai_key = os.getenv("OPENAI_API_KEY")
football_key = os.getenv("FOOTBALL_API_KEY")

print("\n=== API Key Check Results ===")
if openai_key:
    # Don't print the actual key, just the first few and last few characters
    masked_key = openai_key[:4] + "..." + openai_key[-4:] if len(openai_key) > 8 else "***"
    print(f"✅ OPENAI_API_KEY is set: {masked_key}")
else:
    print("❌ OPENAI_API_KEY is not set")

if football_key:
    masked_key = football_key[:4] + "..." + football_key[-4:] if len(football_key) > 8 else "***"
    print(f"✅ FOOTBALL_API_KEY is set: {masked_key}")
else:
    print("❌ FOOTBALL_API_KEY is not set")
    
print("\nIf any keys are missing, please add them to your .env file with the following format:")
print("OPENAI_API_KEY=your_openai_api_key_here")
print("FOOTBALL_API_KEY=your_football_api_key_here")

# Try to import and initialize OpenAI client
try:
    print("\n=== Testing OpenAI Client ===")
    try:
        from openai import OpenAI
        print("✅ Modern OpenAI client package is installed")
        
        client = OpenAI(api_key=openai_key)
        print("✅ OpenAI client initialized with API key")
        
        # Try a simple API call if key is set
        if openai_key:
            print("Testing API with a simple request...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=5
            )
            print(f"✅ API test successful! Response: {response.choices[0].message.content}")
    except ImportError:
        print("❌ Modern OpenAI client not found, trying legacy client...")
        
        import openai
        print("✅ Legacy OpenAI client package is installed")
        
        openai.api_key = openai_key
        print("✅ Set API key in legacy client")
        
        # Try a simple API call if key is set
        if openai_key:
            print("Testing API with a simple request...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=5
            )
            print(f"✅ API test successful! Response: {response.choices[0].message.content}")
            
except Exception as e:
    print(f"❌ Error testing OpenAI client: {str(e)}")
    
print("\nPlease fix any issues identified above and then run your main application.")
