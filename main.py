#!/usr/bin/env python3
"""
LeetCode to GitHub Sync
Main entry point
"""
import sys
from pathlib import Path

from src.config.settings import Settings
from src.services.sync_service import SyncService
from src.utils.logger import setup_logging, get_logger
from src.utils.helpers import parse_date_range_choice


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("  LeetCode to GitHub Sync")
    print("  Automatically sync your LeetCode solutions to GitHub")
    print("=" * 60)
    print()


def get_user_input() -> int:
    """
    Get date range from user
    
    Returns:
        Number of days to look back
    """
    print("How many days back should I fetch submissions?")
    print("  [1] Last 7 days")
    print("  [2] Last 30 days")
    print("  [3] Last 60 days")
    print("  [4] Last 90 days")
    print("  [5] All time")
    print()
    
    choice = input("Enter your choice [1-5] (default: 2): ").strip()
    
    if not choice:
        choice = "2"
    
    days = parse_date_range_choice(choice)
    print()
    
    if days < 0:
        print("✓ Selected: All time")
    else:
        print(f"✓ Selected: Last {days} days")
    print()
    
    return days


def main():
    """Main function"""
    # Print banner
    print_banner()
    
    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        print(f"❌ Error loading settings: {str(e)}")
        return 1
    
    # Setup logging
    setup_logging(log_file=settings.log_file, level=settings.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting LeetCode to GitHub Sync")
    
    # Check if configuration is complete
    if not settings.leetcode_username:
        print("⚠️  LeetCode username not set in config/config.yaml")
        return 1
    
    if not settings.github_username:
        print("⚠️  GitHub username not set in config/config.yaml")
        return 1
    
    if not settings.leetcode_session:
        print("⚠️  LEETCODE_SESSION not set in .env file")
        print("   Please copy env.example to .env and fill in your credentials")
        return 1
    
    if not settings.github_token:
        print("⚠️  GITHUB_TOKEN not set in .env file")
        print("   Please copy env.example to .env and fill in your credentials")
        return 1
    
    # Initialize sync service
    try:
        sync_service = SyncService(settings)
    except Exception as e:
        print(f"❌ Error initializing sync service: {str(e)}")
        logger.error(f"Error initializing sync service: {str(e)}")
        return 1
    
    # Check and create repository if needed
    print("Checking GitHub repository...")
    if not sync_service.github_client.repository_exists():
        print(f"⚠️  Repository '{settings.github_repository}' not found.")
        create = input("Would you like to create it now? [Y/n]: ").strip().lower()
        
        if not create or create in ['y', 'yes']:
            print(f"Creating repository '{settings.github_repository}'...")
            description = f"🚀 LeetCode solutions automatically synced from my LeetCode account"
            
            if sync_service.github_client.create_repository(description):
                print(f"✅ Repository created: https://github.com/{settings.github_username}/{settings.github_repository}")
            else:
                print("❌ Failed to create repository. Please create it manually or check your GitHub token permissions.")
                return 1
        else:
            print("❌ Repository is required. Please create it manually and try again.")
            return 1
    else:
        print(f"✓ Repository '{settings.github_repository}' found")
    
    print()
    
    # Test connections
    print("Testing connections...")
    connections_ok = sync_service.test_connections()
    
    if not connections_ok:
        print("⚠️  Connection test had issues.")
        print()
        proceed = input("Would you like to try syncing anyway? [Y/n]: ").strip().lower()
        
        if proceed and proceed not in ['y', 'yes']:
            print("❌ Sync cancelled. Please check your credentials.")
            print()
            print("To fix LeetCode connection:")
            print("  1. Go to leetcode.com and logout/login")
            print("  2. Get fresh cookies (F12 → Application → Cookies)")
            print("  3. Update .env file with new LEETCODE_SESSION and csrftoken")
            return 1
        
        print("⚠️  Proceeding with sync attempt...")
        print("   (The actual sync might work even if connection test failed)")
    
    print()
    
    # Get user input for date range
    days_back = get_user_input()
    
    # Confirm before proceeding
    print(f"Configuration:")
    print(f"  LeetCode User: {settings.leetcode_username}")
    print(f"  GitHub Repo: {settings.github_username}/{settings.github_repository}")
    print(f"  Active Tags: {', '.join(settings.active_tags)}")
    print(f"  Date Range: {'All time' if days_back < 0 else f'Last {days_back} days'}")
    print()
    
    confirm = input("Proceed with sync? [Y/n]: ").strip().lower()
    if confirm and confirm not in ['y', 'yes']:
        print("Sync cancelled.")
        return 0
    
    print()
    
    # Run sync
    try:
        result = sync_service.sync(days_back=days_back if days_back >= 0 else 0)
        
        # Print results
        print()
        print("=" * 60)
        print("Sync Results")
        print("=" * 60)
        print(f"Total submissions found: {result.total_submissions}")
        print(f"Filtered submissions: {result.filtered_submissions}")
        print(f"Files created/updated: {result.files_created}")
        print(f"Files skipped: {result.files_skipped}")
        print(f"Errors: {len(result.errors)}")
        print(f"Duration: {result.duration:.2f} seconds")
        print()
        
        if result.tag_counts:
            print("Files by category:")
            for tag, count in result.tag_counts.items():
                print(f"  {tag}: {count} files")
            print()
        
        if result.errors:
            print("Errors encountered:")
            for error in result.errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(result.errors) > 5:
                print(f"  ... and {len(result.errors) - 5} more")
            print()
        
        print(f"✅ Sync completed successfully!")
        print(f"🔗 View your solutions: {sync_service.github_client.get_repository_url()}")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\n❌ Sync failed: {str(e)}")
        logger.error(f"Sync failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
