#!/usr/bin/env python3
"""
Quick script to create the GitHub repository
"""
import os
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv()

# Get credentials
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("❌ GITHUB_TOKEN not found in .env file")
    exit(1)

# Initialize GitHub client
print("Creating GitHub repository...")
print()

try:
    g = Github(github_token)
    user = g.get_user()
    
    print(f"✓ Connected as: {user.login}")
    
    # Create repository
    repo = user.create_repo(
        name="leetcode-solutions",
        description="🚀 LeetCode solutions automatically synced from my LeetCode account",
        private=False,  # Change to True if you want it private
        auto_init=True,  # Initialize with README
        has_issues=True,
        has_wiki=False,
        has_downloads=True
    )
    
    print(f"✅ Repository created successfully!")
    print(f"🔗 URL: {repo.html_url}")
    print()
    print("Repository Details:")
    print(f"  - Name: {repo.name}")
    print(f"  - Visibility: {'Private' if repo.private else 'Public'}")
    print(f"  - Default Branch: {repo.default_branch}")
    print()
    print("✅ You can now run: python3 main.py")
    
except Exception as e:
    if "already exists" in str(e).lower():
        print("✓ Repository 'leetcode-solutions' already exists!")
        print(f"🔗 URL: https://github.com/{user.login}/leetcode-solutions")
        print()
        print("✅ You can now run: python3 main.py")
    else:
        print(f"❌ Error creating repository: {str(e)}")
        exit(1)
