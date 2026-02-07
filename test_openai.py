#!/usr/bin/env python3
"""
Simple script to test OpenAI API key
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("❌ Error: OPENAI_API_KEY not found in environment variables")
    print("Make sure you have added it to your .env file")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

print("🔑 Testing OpenAI API key...")
print("-" * 50)

try:
    # Simple test: list available models
    print("\n📋 Fetching available models...")
    models = client.models.list()
    
    # Get a few model names to verify connection works
    model_names = [model.id for model in models.data[:5]]
    print(f"✅ Successfully connected to OpenAI API!")
    print(f"📦 Found {len(models.data)} models")
    print(f"   Sample models: {', '.join(model_names)}")
    
    # Test a simple completion
    print("\n💬 Testing a simple chat completion...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello! Your API key is working!' in one sentence."}
        ],
        max_tokens=50
    )
    
    message = response.choices[0].message.content
    print(f"✅ Chat completion successful!")
    print(f"🤖 Response: {message}")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Your OpenAI API key is working correctly.")
    print("=" * 50)
    
except Exception as e:
    error_msg = str(e)
    
    if "insufficient_quota" in error_msg or "429" in error_msg:
        print(f"\n⚠️  Quota/Billing Issue: {error_msg}")
        print("\n✅ Your API key is VALID and working!")
        print("❌ But your account has no credits or exceeded quota.")
        print("\nTo fix this:")
        print("  1. Go to https://platform.openai.com/account/billing")
        print("  2. Add payment method or credits")
        print("  3. Check your usage limits")
    elif "401" in error_msg or "invalid" in error_msg.lower():
        print(f"\n❌ Invalid API Key: {error_msg}")
        print("  - Check that your API key is correct")
        print("  - Make sure it starts with 'sk-'")
    else:
        print(f"\n❌ Error: {error_msg}")
        print("\nPossible issues:")
        print("  - Network connection problem")
        print("  - API service temporarily unavailable")
    exit(1)
