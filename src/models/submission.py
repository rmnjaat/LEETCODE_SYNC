"""
Submission data model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.config.enums import SubmissionStatus, Language, FileExtension
from src.models.problem import Problem


@dataclass
class Submission:
    """Submission details from LeetCode"""
    id: str
    code: str
    timestamp: int  # Unix timestamp
    status: str
    language: str
    runtime: Optional[str]
    memory: Optional[str]
    problem: Problem
    
    @property
    def datetime(self) -> datetime:
        """Get submission datetime"""
        return datetime.fromtimestamp(int(self.timestamp))
    
    @property
    def is_accepted(self) -> bool:
        """Check if submission was accepted"""
        return self.status == "Accepted"
    
    @property
    def file_extension(self) -> str:
        """Get file extension for this language"""
        try:
            lang_enum = Language[self.language.upper()]
            return FileExtension[lang_enum.name].value
        except KeyError:
            # Default to .txt for unknown languages
            return ".txt"
    
    @property
    def formatted_timestamp(self) -> str:
        """Get formatted timestamp string"""
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def timestamp_for_filename(self) -> str:
        """Get timestamp for filename (no special chars)"""
        return self.datetime.strftime("%Y%m%d_%H%M%S")
    
    def __repr__(self) -> str:
        return f"Submission({self.id}, {self.problem.title}, {self.status})"
