"""
GitHub API client
Handles all interactions with GitHub API
"""
from typing import Optional, List
from github import Github, GithubException
from github.Repository import Repository
from github.ContentFile import ContentFile
import base64

from src.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """Client for GitHub API using PyGithub"""
    
    def __init__(self, token: str, username: str, repository: str):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub Personal Access Token
            username: GitHub username
            repository: Repository name
        """
        self.token = token
        self.username = username
        self.repository_name = repository
        self.github = Github(token)
        self.repo: Optional[Repository] = None
        self._connect_to_repo()
    
    def _connect_to_repo(self):
        """Connect to the GitHub repository"""
        try:
            repo_full_name = f"{self.username}/{self.repository_name}"
            self.repo = self.github.get_repo(repo_full_name)
            logger.info(f"✓ Connected to repository: {repo_full_name}")
        except GithubException as e:
            logger.error(f"✗ Failed to connect to repository: {str(e)}")
            self.repo = None
    
    def test_connection(self) -> bool:
        """
        Test if connection to GitHub is working
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            user = self.github.get_user()
            logger.info(f"✓ GitHub connection test successful (User: {user.login})")
            return True
        except Exception as e:
            logger.error(f"✗ GitHub connection test failed: {str(e)}")
            return False
    
    def repository_exists(self) -> bool:
        """Check if repository exists"""
        return self.repo is not None
    
    def create_repository(self, description: str = "LeetCode solutions synced automatically") -> bool:
        """
        Create a new repository
        
        Args:
            description: Repository description
            
        Returns:
            True if created successfully, False otherwise
        """
        try:
            user = self.github.get_user()
            self.repo = user.create_repo(
                name=self.repository_name,
                description=description,
                private=False,
                auto_init=True
            )
            logger.info(f"✓ Created repository: {self.repository_name}")
            return True
        except GithubException as e:
            logger.error(f"✗ Failed to create repository: {str(e)}")
            return False
    
    def file_exists(self, file_path: str, branch: str = "main") -> bool:
        """
        Check if a file exists in the repository
        
        Args:
            file_path: Path to file in repository
            branch: Branch name
            
        Returns:
            True if file exists, False otherwise
        """
        if not self.repo:
            return False
        
        try:
            self.repo.get_contents(file_path, ref=branch)
            return True
        except GithubException:
            return False
    
    def get_file_content(self, file_path: str, branch: str = "main") -> Optional[str]:
        """
        Get content of a file
        
        Args:
            file_path: Path to file in repository
            branch: Branch name
            
        Returns:
            File content as string or None if not found
        """
        if not self.repo:
            return None
        
        try:
            content_file = self.repo.get_contents(file_path, ref=branch)
            if isinstance(content_file, list):
                return None
            return content_file.decoded_content.decode('utf-8')
        except GithubException:
            return None
    
    def create_or_update_file(self, file_path: str, content: str, 
                             commit_message: str, branch: str = "main") -> bool:
        """
        Create a new file or update existing file
        
        Args:
            file_path: Path to file in repository
            content: File content
            commit_message: Commit message
            branch: Branch name
            
        Returns:
            True if successful, False otherwise
        """
        if not self.repo:
            logger.error("No repository connection")
            return False
        
        try:
            # Check if file exists
            try:
                existing_file = self.repo.get_contents(file_path, ref=branch)
                # File exists, update it
                if isinstance(existing_file, list):
                    logger.error(f"Path is a directory: {file_path}")
                    return False
                
                self.repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha,
                    branch=branch
                )
                logger.info(f"✓ Updated file: {file_path}")
                return True
                
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        path=file_path,
                        message=commit_message,
                        content=content,
                        branch=branch
                    )
                    logger.info(f"✓ Created file: {file_path}")
                    return True
                else:
                    raise
        
        except GithubException as e:
            logger.error(f"✗ Failed to create/update file {file_path}: {str(e)}")
            return False
    
    def create_folder(self, folder_path: str, branch: str = "main") -> bool:
        """
        Create a folder by adding a .gitkeep file
        
        Args:
            folder_path: Path to folder
            branch: Branch name
            
        Returns:
            True if successful, False otherwise
        """
        gitkeep_path = f"{folder_path}/.gitkeep"
        return self.create_or_update_file(
            file_path=gitkeep_path,
            content="",
            commit_message=f"Create folder: {folder_path}",
            branch=branch
        )
    
    def bulk_upload_files(self, files: List[tuple], commit_message: str, 
                         branch: str = "main") -> int:
        """
        Upload multiple files in separate commits
        
        Args:
            files: List of (file_path, content) tuples
            commit_message: Base commit message
            branch: Branch name
            
        Returns:
            Number of files successfully uploaded
        """
        success_count = 0
        
        for file_path, content in files:
            specific_message = f"{commit_message}: {file_path}"
            if self.create_or_update_file(file_path, content, specific_message, branch):
                success_count += 1
        
        logger.info(f"✓ Uploaded {success_count}/{len(files)} files")
        return success_count
    
    def get_repository_url(self) -> str:
        """Get repository URL"""
        if self.repo:
            return self.repo.html_url
        return f"https://github.com/{self.username}/{self.repository_name}"
