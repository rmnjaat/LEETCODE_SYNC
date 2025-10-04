"""
Solution organizer service
Organizes submissions by tags and handles multiple versions
"""
from typing import List, Dict, Tuple
from collections import defaultdict

from src.models.submission import Submission
from src.utils.helpers import slug_to_filename
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SolutionOrganizer:
    """Organizes solutions by tags and manages versions"""
    
    def __init__(self, tag_mappings: Dict[str, str], active_tags: List[str]):
        """
        Initialize organizer
        
        Args:
            tag_mappings: Dictionary mapping LeetCode tags to folder names
            active_tags: List of tags to sync
        """
        self.tag_mappings = tag_mappings
        self.active_tags = [tag.lower() for tag in active_tags]
    
    def filter_by_tags(self, submissions: List[Submission]) -> List[Submission]:
        """
        Filter submissions to only include active tags
        
        Args:
            submissions: List of all submissions
            
        Returns:
            Filtered list of submissions
        """
        filtered = []
        
        for submission in submissions:
            problem_tags = [tag.lower() for tag in submission.problem.tags]
            
            # Check if problem has any active tags
            if any(tag in problem_tags for tag in self.active_tags):
                filtered.append(submission)
        
        logger.info(f"Filtered {len(filtered)} submissions matching active tags")
        return filtered
    
    def get_folder_for_submission(self, submission: Submission) -> str:
        """
        Get target folder for a submission based on tags
        
        Args:
            submission: Submission object
            
        Returns:
            Folder name
        """
        problem_tags = submission.problem.tags
        
        # Find first matching tag
        for tag in problem_tags:
            tag_lower = tag.lower()
            
            # Check if this tag is active
            if tag_lower in self.active_tags:
                # Get folder mapping
                for map_tag, folder_name in self.tag_mappings.items():
                    if map_tag.lower() == tag_lower:
                        return folder_name
        
        # Default folder if no match
        return "Others"
    
    def group_by_problem(self, submissions: List[Submission]) -> Dict[str, List[Submission]]:
        """
        Group submissions by problem slug
        
        Args:
            submissions: List of submissions
            
        Returns:
            Dictionary mapping problem slug to list of submissions
        """
        grouped = defaultdict(list)
        
        for submission in submissions:
            slug = submission.problem.title_slug
            grouped[slug].append(submission)
        
        # Sort each group by timestamp
        for slug in grouped:
            grouped[slug].sort(key=lambda x: x.timestamp)
        
        return dict(grouped)
    
    def organize_files(self, submissions: List[Submission]) -> List[Tuple[str, Submission, int]]:
        """
        Organize submissions into file paths with version numbers
        
        Args:
            submissions: List of submissions
            
        Returns:
            List of tuples: (file_path, submission, version)
        """
        # Group by problem
        grouped = self.group_by_problem(submissions)
        
        file_list = []
        
        for slug, problem_submissions in grouped.items():
            folder = self.get_folder_for_submission(problem_submissions[0])
            
            # If only one submission, no version number
            if len(problem_submissions) == 1:
                sub = problem_submissions[0]
                filename = slug_to_filename(slug, 0, sub.file_extension)
                file_path = f"{folder}/{filename}"
                file_list.append((file_path, sub, 0))
            else:
                # Multiple submissions - add version numbers
                for version, sub in enumerate(problem_submissions, 1):
                    filename = slug_to_filename(slug, version, sub.file_extension)
                    file_path = f"{folder}/{filename}"
                    file_list.append((file_path, sub, version))
        
        logger.info(f"Organized {len(file_list)} files across {len(grouped)} problems")
        return file_list
    
    def get_statistics(self, submissions: List[Submission]) -> Dict:
        """
        Get statistics about submissions
        
        Args:
            submissions: List of submissions
            
        Returns:
            Dictionary of statistics
        """
        stats = {
            "total": len(submissions),
            "easy": 0,
            "medium": 0,
            "hard": 0,
            "by_tag": defaultdict(int),
            "unique_problems": len(set(sub.problem.title_slug for sub in submissions))
        }
        
        for sub in submissions:
            # Count by difficulty
            diff = sub.problem.difficulty.lower()
            if diff == "easy":
                stats["easy"] += 1
            elif diff == "medium":
                stats["medium"] += 1
            elif diff == "hard":
                stats["hard"] += 1
            
            # Count by tag
            for tag in sub.problem.tags:
                stats["by_tag"][tag] += 1
        
        return stats
