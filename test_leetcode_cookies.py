#!/usr/bin/env python3
"""
Test script to validate LeetCode cookies
"""
import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

session_cookie = os.getenv('LEETCODE_SESSION')
csrf_token = os.getenv('LEETCODE_CSRF_TOKEN')

print("=" * 60)
print("  🧪 LeetCode Cookie Validation Test")
print("=" * 60)
print()

# Check if cookies exist
print("1️⃣  Checking if cookies are present...")
if not session_cookie:
    print("   ❌ LEETCODE_SESSION is missing in .env file")
    exit(1)
else:
    print(f"   ✅ LEETCODE_SESSION found ({len(session_cookie)} chars)")

if not csrf_token:
    print("   ❌ LEETCODE_CSRF_TOKEN is missing in .env file")
    exit(1)
else:
    print(f"   ✅ LEETCODE_CSRF_TOKEN found ({len(csrf_token)} chars)")

print()

# Test 1: Basic website access
print("2️⃣  Testing basic LeetCode website access...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

try:
    response = requests.get('https://leetcode.com', headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"   ✅ LeetCode website accessible (Status: {response.status_code})")
    else:
        print(f"   ⚠️  Unusual status code: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cannot access LeetCode: {str(e)}")
    exit(1)

print()

# Test 2: GraphQL API with authentication
print("3️⃣  Testing GraphQL API with your cookies...")
graphql_url = "https://leetcode.com/graphql"

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': f'LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}',
    'x-csrftoken': csrf_token,
    'Referer': 'https://leetcode.com',
}

# Simple query to test authentication
query = """
query globalData {
  userStatus {
    username
    isSignedIn
    isPremium
  }
}
"""

try:
    response = requests.post(
        graphql_url,
        json={'query': query},
        headers=headers,
        timeout=10
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if 'errors' in data:
            print(f"   ❌ GraphQL errors: {data['errors']}")
            print()
            print("   💡 This usually means:")
            print("      - Session cookie is expired")
            print("      - Cookie format is incorrect")
            print("      - You need to logout/login again")
        elif 'data' in data and data['data'].get('userStatus'):
            user_status = data['data']['userStatus']
            
            if user_status.get('isSignedIn'):
                print(f"   ✅ Authentication SUCCESSFUL!")
                print(f"   ✅ Logged in as: {user_status.get('username', 'Unknown')}")
                print(f"   ✅ Premium: {user_status.get('isPremium', False)}")
                print()
                print("   🎉 Your cookies are VALID and working!")
            else:
                print("   ❌ Not signed in (cookies invalid or expired)")
                print()
                print("   💡 Solution: Get fresh cookies")
        else:
            print(f"   ⚠️  Unexpected response format")
            print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Request failed: {str(e)}")

print()

# Test 3: Check cookie format
print("4️⃣  Validating cookie format...")

# LEETCODE_SESSION should be a JWT token
if session_cookie.startswith('eyJ'):
    print("   ✅ LEETCODE_SESSION appears to be a valid JWT token")
else:
    print("   ⚠️  LEETCODE_SESSION doesn't look like a JWT token")
    print("   💡 Make sure you copied the ENTIRE value")

# CSRF token should be alphanumeric
if csrf_token and len(csrf_token) >= 32 and csrf_token.isalnum():
    print("   ✅ CSRF token format looks correct")
else:
    print("   ⚠️  CSRF token format looks unusual")

print()
print("=" * 60)
print()

# Final recommendations
print("📋 RECOMMENDATIONS:")
print()

if session_cookie.startswith('eyJ'):
    print("✅ Cookie format looks good")
    print()
    print("If authentication still fails:")
    print("  1. Cookies might be expired (try logout/login)")
    print("  2. Make sure you're copying from the RIGHT domain:")
    print("     → Use https://leetcode.com (NOT leetcode.cn)")
    print("  3. Copy the ENTIRE cookie value (no spaces)")
    print("  4. Make sure .env file has no extra quotes or spaces")
else:
    print("⚠️  Cookie format issues detected")
    print()
    print("To get correct cookies:")
    print("  1. Go to https://leetcode.com (make sure it's .com!)")
    print("  2. Logout completely")
    print("  3. Login again")
    print("  4. F12 → Application → Cookies → https://leetcode.com")
    print("  5. Copy LEETCODE_SESSION value (starts with 'eyJ')")
    print("  6. Copy csrftoken value")
    print("  7. Update .env file")

print()
print("=" * 60)
