"""
LeetCode API client
Handles all interactions with LeetCode GraphQL API
"""
import requests
import time
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from src.config.constants import (
    LEETCODE_GRAPHQL_ENDPOINT,
    GRAPHQL_RECENT_SUBMISSIONS,
    GRAPHQL_SUBMISSION_DETAIL,
    DEFAULT_SUBMISSION_LIMIT,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_DELAY
)
from src.models.problem import Problem
from src.models.submission import Submission
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LeetCodeClient:
    """Client for LeetCode GraphQL API"""
    
    def __init__(self, session_cookie: str, csrf_token: Optional[str] = None):
        """
        Initialize LeetCode client
        
        Args:
            session_cookie: LEETCODE_SESSION cookie value
            csrf_token: CSRF token (optional)
        """
        self.session_cookie = session_cookie
        self.csrf_token = csrf_token or ""
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup requests session with headers"""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Cookie": f"LEETCODE_SESSION={self.session_cookie}; csrftoken={self.csrf_token}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://leetcode.com",
            "X-CSRFToken": self.csrf_token
        })
    
    def _make_request(self, query: str, variables: Dict[str, Any], 
                     retry_attempts: int = DEFAULT_RETRY_ATTEMPTS) -> Optional[Dict]:
        """
        Make GraphQL request with retry logic
        
        Args:
            query: GraphQL query string
            variables: Query variables
            retry_attempts: Number of retry attempts
            
        Returns:
            Response data or None if failed
        """
        payload = {
            "query": query,
            "variables": variables
        }
        
        for attempt in range(retry_attempts):
            try:
                response = self.session.post(
                    LEETCODE_GRAPHQL_ENDPOINT,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "errors" in data:
                        logger.error(f"GraphQL errors: {data['errors']}")
                        return None
                    return data.get("data")
                elif response.status_code == 400:
                    logger.warning(f"Bad request (400) - possibly rate limited or invalid submission ID")
                    return None
                elif response.status_code == 429:
                    logger.warning(f"Rate limited (429) - waiting longer...")
                    time.sleep(5)
                    continue
                else:
                    logger.warning(f"Request failed with status {response.status_code}")
                
            except Exception as e:
                logger.error(f"Request error (attempt {attempt + 1}): {str(e)}")
            
            if attempt < retry_attempts - 1:
                time.sleep(DEFAULT_RETRY_DELAY)
        
        return None
    
    def get_recent_submissions(self, username: str, 
                              limit: int = DEFAULT_SUBMISSION_LIMIT) -> List[Dict]:
        """
        Get list of recent submissions
        
        Args:
            username: LeetCode username
            limit: Maximum number of submissions to fetch
            
        Returns:
            List of submission summaries
        """
        logger.info(f"Fetching recent submissions for user: {username}")
        
        variables = {
            "username": username,
            "limit": limit
        }
        
        data = self._make_request(GRAPHQL_RECENT_SUBMISSIONS, variables)
        
        if data and "recentAcSubmissionList" in data:
            submissions = data["recentAcSubmissionList"]
            logger.info(f"Found {len(submissions)} recent submissions")
            return submissions
        
        logger.error("Failed to fetch recent submissions")
        return []
    
    def get_submission_detail(self, submission_id: int) -> Optional[Submission]:
        """
        Get detailed submission information including code
        
        Args:
            submission_id: Submission ID
            
        Returns:
            Submission object or None if failed
        """
        logger.debug(f"Fetching submission detail for ID: {submission_id}")
        
        variables = {"submissionId": submission_id}
        data = self._make_request(GRAPHQL_SUBMISSION_DETAIL, variables)
        
        if not data or "submissionDetails" not in data:
            logger.warning(f"Failed to fetch submission {submission_id} - skipping")
            return None
        
        detail = data["submissionDetails"]
        
        # Check if submission detail is valid
        if not detail or detail.get("code") is None:
            logger.warning(f"Submission {submission_id} has no code - skipping")
            return None
        
        question = detail.get("question", {})
        
        # Parse problem
        problem = Problem(
            question_id=question.get("questionId", ""),
            title=question.get("title", ""),
            title_slug=question.get("titleSlug", ""),
            content=question.get("content", ""),
            difficulty=question.get("difficulty", "Unknown"),
            tags=[tag.get("name", "") for tag in question.get("topicTags", [])]
        )
        
        # Parse submission
        lang_info = detail.get("lang", {})
        language_name = lang_info.get("name", "") if isinstance(lang_info, dict) else str(lang_info)
        
        submission = Submission(
            id=detail.get("id", ""),
            code=detail.get("code", ""),
            timestamp=int(detail.get("timestamp", 0)),
            status="Accepted",  # We only fetch accepted submissions
            language=language_name,
            runtime=detail.get("runtimeDisplay"),
            memory=detail.get("memoryDisplay"),
            problem=problem
        )
        
        logger.debug(f"Successfully fetched submission: {submission.problem.title}")
        return submission
    
    def get_submissions_by_date_range(self, username: str, days_back: int) -> List[Submission]:
        """
        Get submissions within a date range
        
        Args:
            username: LeetCode username
            days_back: Number of days to look back
            
        Returns:
            List of Submission objects
        """
        logger.info(f"Fetching submissions from last {days_back} days")
        
        # Get recent submission list
        recent_submissions = self.get_recent_submissions(username)
        
        if not recent_submissions:
            return []
        
        # Calculate cutoff timestamp
        cutoff_date = datetime.now() - timedelta(days=days_back)
        cutoff_timestamp = int(cutoff_date.timestamp())
        
        logger.info(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Filter by date and fetch details
        filtered_submissions = []
        
        for sub_summary in recent_submissions:
            timestamp = int(sub_summary.get("timestamp", 0))
            
            # Check if within date range
            if days_back > 0 and timestamp < cutoff_timestamp:
                continue
            
            # Fetch full submission details
            submission_id = int(sub_summary.get("id", 0))
            submission = self.get_submission_detail(submission_id)
            
            if submission:
                filtered_submissions.append(submission)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        logger.info(f"Filtered to {len(filtered_submissions)} submissions within date range")
        return filtered_submissions
    
    def test_connection(self) -> bool:
        """
        Test if connection to LeetCode is working
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test with a simple GraphQL query
            query = """
            query globalData {
              userStatus {
                username
                isSignedIn
              }
            }
            """
              
            data = self._make_request(query, {})
            
            if data and 'userStatus' in data:
                user_status = data['userStatus']
                if user_status.get('isSignedIn'):
                    username = user_status.get('username', 'Unknown')
                    logger.info(f"✓ LeetCode connection test successful (User: {username})")
                    return True
                else:
                    logger.error("✗ LeetCode connection test failed: Not signed in")
                    return False
            else:
                logger.error("✗ LeetCode connection test failed: Invalid response")
                return False
                
        except Exception as e:
            logger.error(f"✗ LeetCode connection test failed: {str(e)}")
            return False
