#!/usr/bin/env python3
"""
Test script to check if we can fetch submissions
"""
import os
from dotenv import load_dotenv
from src.config.settings import Settings
from src.core.leetcode_client import LeetCodeClient

load_dotenv()

print("=" * 60)
print("  🧪 Testing LeetCode Submissions Fetch")
print("=" * 60)
print()

settings = Settings()
client = LeetCodeClient(settings.leetcode_session, settings.leetcode_csrf)

print("1️⃣  Testing connection...")
if not client.test_connection():
    print("❌ Connection failed")
    exit(1)
print("✅ Connection successful")
print()

print("2️⃣  Fetching recent submissions list...")
recent = client.get_recent_submissions(settings.leetcode_username, limit=5)
print(f"✅ Found {len(recent)} recent submissions")
print()

if not recent:
    print("❌ No submissions found")
    exit(1)

print("3️⃣  Testing submission detail fetch...")
print("(This might take a moment due to rate limiting)")
print()

success_count = 0
for i, sub in enumerate(recent[:3]):  # Test first 3
    print(f"   Testing submission {i+1}/3: {sub.get('title', 'Unknown')}")
    detail = client.get_submission_detail(int(sub.get('id', 0)))
    
    if detail:
        print(f"   ✅ Success: {detail.problem.title}")
        success_count += 1
    else:
        print(f"   ⚠️  Failed to fetch details")
    print()

print("=" * 60)
print(f"📊 RESULTS: {success_count}/3 submissions fetched successfully")
print()

if success_count > 0:
    print("✅ The sync should work! Some submissions are accessible.")
    print("💡 The 400 errors are normal - not all submissions are accessible.")
    print("   The app will skip failed ones and sync the successful ones.")
else:
    print("❌ No submissions could be fetched.")
    print("💡 This might be due to:")
    print("   - Rate limiting")
    print("   - LeetCode API changes")
    print("   - Account permissions")

print("=" * 60)
