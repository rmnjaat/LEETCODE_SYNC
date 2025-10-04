"""
Main sync service
Orchestrates the sync process
"""
from typing import List, Optional
from datetime import datetime

from src.core.leetcode_client import LeetCodeClient
from src.core.github_client import GitHubClient
from src.services.solution_organizer import SolutionOrganizer
from src.services.file_formatter import FileFormatter
from src.models.submission import Submission
from src.models.sync_result import SyncResult
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SyncService:
    """Main service for syncing LeetCode submissions to GitHub"""
    
    def __init__(self, settings: Settings):
        """
        Initialize sync service
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        
        # Initialize clients
        self.leetcode_client = LeetCodeClient(
            session_cookie=settings.leetcode_session,
            csrf_token=settings.leetcode_csrf
        )
        
        self.github_client = GitHubClient(
            token=settings.github_token,
            username=settings.github_username,
            repository=settings.github_repository
        )
        
        # Initialize services
        self.organizer = SolutionOrganizer(
            tag_mappings=settings.tag_folder_mappings,
            active_tags=settings.active_tags
        )
        
        self.formatter = FileFormatter()
    
    def test_connections(self) -> bool:
        """
        Test connections to LeetCode and GitHub
        
        Returns:
            True if both connections successful
        """
        logger.info("Testing connections...")
        
        leetcode_ok = self.leetcode_client.test_connection()
        github_ok = self.github_client.test_connection()
        
        if leetcode_ok and github_ok:
            logger.info("✓ All connections successful")
            return True
        else:
            logger.error("✗ Connection test failed")
            return False
    
    def sync(self, days_back: Optional[int] = None) -> SyncResult:
        """
        Main sync operation
        
        Args:
            days_back: Number of days to look back (None = use config)
            
        Returns:
            SyncResult object
        """
        result = SyncResult()
        result.start_time = datetime.now()
        
        logger.info("=" * 60)
        logger.info("Starting LeetCode to GitHub sync...")
        logger.info("=" * 60)
        
        try:
            # Use provided days or config
            if days_back is None:
                days_back = self.settings.days_to_look_back
            
            # Fetch submissions
            logger.info(f"Fetching submissions from last {days_back} days...")
            submissions = self.leetcode_client.get_submissions_by_date_range(
                username=self.settings.leetcode_username,
                days_back=days_back
            )
            
            result.total_submissions = len(submissions)
            logger.info(f"✓ Found {len(submissions)} total submissions")
            
            if not submissions:
                logger.warning("No submissions found")
                result.finish()
                return result
            
            # Filter by status (accepted only)
            if self.settings.only_accepted:
                submissions = [s for s in submissions if s.is_accepted]
                logger.info(f"✓ Filtered to {len(submissions)} accepted submissions")
            
            # Filter by tags
            submissions = self.organizer.filter_by_tags(submissions)
            result.filtered_submissions = len(submissions)
            
            if not submissions:
                logger.warning("No submissions match the active tags")
                result.finish()
                return result
            
            # Get statistics
            stats = self.organizer.get_statistics(submissions)
            logger.info(f"✓ Found {stats['unique_problems']} unique problems")
            logger.info(f"  Easy: {stats['easy']} | Medium: {stats['medium']} | Hard: {stats['hard']}")
            
            # Organize into files
            file_list = self.organizer.organize_files(submissions)
            logger.info(f"✓ Organized into {len(file_list)} files")
            
            # Check for multiple versions
            multi_version_problems = sum(1 for _, _, version in file_list if version > 1)
            if multi_version_problems > 0:
                logger.info(f"ℹ  Found {multi_version_problems} problems with multiple solutions")
            
            # Upload to GitHub
            logger.info("Uploading to GitHub...")
            
            for file_path, submission, version in file_list:
                try:
                    # Format file content
                    content = self.formatter.format_solution_file(
                        submission,
                        version if version > 0 else None
                    )
                    
                    # Create commit message
                    if version > 0:
                        commit_msg = f"Add: {submission.problem.title} (v{version})"
                    else:
                        commit_msg = f"Add: {submission.problem.title}"
                    
                    # Upload file
                    success = self.github_client.create_or_update_file(
                        file_path=file_path,
                        content=content,
                        commit_message=commit_msg,
                        branch=self.settings.github_branch
                    )
                    
                    if success:
                        result.files_created += 1
                        result.add_synced_problem(submission.problem.title)
                        
                        # Track by tag
                        folder = self.organizer.get_folder_for_submission(submission)
                        result.increment_tag_count(folder)
                    else:
                        result.files_skipped += 1
                        result.add_error(f"Failed to upload: {file_path}")
                
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    result.add_error(f"{file_path}: {str(e)}")
                    result.files_skipped += 1
            
            # Summary
            logger.info("=" * 60)
            logger.info("Sync completed!")
            logger.info(f"✓ Files created/updated: {result.files_created}")
            logger.info(f"  Skipped: {result.files_skipped}")
            logger.info(f"  Errors: {len(result.errors)}")
            logger.info(f"✓ Repository: {self.github_client.get_repository_url()}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            result.add_error(f"Sync failed: {str(e)}")
        
        result.finish()
        return result
