"""
Sync result data model
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class SyncResult:
    """Result of a sync operation"""
    total_submissions: int = 0
    filtered_submissions: int = 0
    files_created: int = 0
    files_updated: int = 0
    files_skipped: int = 0
    errors: List[str] = field(default_factory=list)
    synced_problems: List[str] = field(default_factory=list)
    tag_counts: Dict[str, int] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def duration(self) -> float:
        """Get sync duration in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    @property
    def success_rate(self) -> float:
        """Get success rate percentage"""
        total = self.files_created + self.files_updated + self.files_skipped
        if total == 0:
            return 0.0
        return ((self.files_created + self.files_updated) / total) * 100
    
    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(error)
    
    def add_synced_problem(self, problem_title: str):
        """Add a synced problem"""
        if problem_title not in self.synced_problems:
            self.synced_problems.append(problem_title)
    
    def increment_tag_count(self, tag: str):
        """Increment count for a tag"""
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
    
    def finish(self):
        """Mark sync as finished"""
        self.end_time = datetime.now()
    
    def __repr__(self) -> str:
        return (f"SyncResult(created={self.files_created}, "
                f"updated={self.files_updated}, "
                f"errors={len(self.errors)})")
