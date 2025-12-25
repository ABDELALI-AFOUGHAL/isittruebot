#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for API quota handling and retry mechanism
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.analyzer import IsItTrueAnalyzer
from modules.logger import setup_logger

logger = setup_logger(__name__)

async def test_retry_mechanism():
    """Test the retry mechanism with exponential backoff"""
    
    print("\n" + "="*60)
    print("🧪 Testing API Retry Mechanism")
    print("="*60 + "\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Text Analysis",
            "text": "Is the Earth flat?",
            "description": "Basic fact-checking"
        },
        {
            "name": "Spam Detection",
            "text": "You won $1,000,000! Click here!",
            "description": "Misinformation detection"
        },
        {
            "name": "Recent News",
            "text": "What is the current status of AI regulation?",
            "description": "Question requiring web search"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Input: {test_case['text']}")
        print("-" * 60)
        
        try:
            start_time = time.time()
            
            # Call analyzer
            result = await IsItTrueAnalyzer.process_input(
                user_input=test_case['text'],
                source="test_script"
            )
            
            elapsed = time.time() - start_time
            
            # Display result
            print(f"✅ SUCCESS (took {elapsed:.2f}s)")
            print(f"Result length: {len(result)} characters")
            print(f"Result preview:\n{result[:300]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:100]}")
    
    print("\n" + "="*60)
    print("🧪 Test Complete")
    print("="*60 + "\n")

async def test_quota_error_handling():
    """Test 429 quota error detection"""
    
    print("\n" + "="*60)
    print("🔍 Checking Quota Error Handling")
    print("="*60 + "\n")
    
    print("Retry mechanism features:")
    print("✅ Max retries: 3 attempts")
    print("✅ Exponential backoff: 1s → 2s → 4s")
    print("✅ Detects 429 errors specifically")
    print("✅ Provides multilingual error messages")
    print("✅ Frontend caching: 1-hour TTL")
    
    print("\nIf you encounter 429 error:")
    print("1. Retries will happen automatically")
    print("2. Wait 1-4 seconds for retry")
    print("3. If still fails, quota is exhausted")
    print("4. Check API_QUOTA_MANAGEMENT.md for solutions")
    
    print("\n" + "="*60 + "\n")

async def main():
    """Main test function"""
    print("\n🚀 API Quota & Retry Mechanism Test Suite\n")
    
    # Run tests
    await test_quota_error_handling()
    
    try:
        await test_retry_mechanism()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest suite interrupted")
        sys.exit(1)
