"""
Problem data model
"""
from dataclasses import dataclass
from typing import List

from src.config.enums import Difficulty


@dataclass
class Problem:
    """Problem details from LeetCode"""
    question_id: str
    title: str
    title_slug: str
    content: str
    difficulty: str
    tags: List[str]
    
    @property
    def url(self) -> str:
        """Get LeetCode problem URL"""
        return f"https://leetcode.com/problems/{self.title_slug}/"
    
    @property
    def difficulty_enum(self) -> Difficulty:
        """Get difficulty as enum"""
        return Difficulty(self.difficulty)
    
    def has_tag(self, tag: str) -> bool:
        """Check if problem has a specific tag"""
        return tag.lower() in [t.lower() for t in self.tags]
    
    def __repr__(self) -> str:
        return f"Problem({self.question_id}. {self.title})"
