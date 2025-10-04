"""
Helper utility functions
"""
import re
from typing import List
from src.config.constants import INVALID_FILENAME_CHARS, MAX_FILENAME_LENGTH


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    for char in INVALID_FILENAME_CHARS:
        filename = filename.replace(char, '-')
    
    # Replace multiple hyphens with single hyphen
    filename = re.sub(r'-+', '-', filename)
    
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    
    # Limit length
    if len(filename) > MAX_FILENAME_LENGTH:
        filename = filename[:MAX_FILENAME_LENGTH]
    
    return filename


def slug_to_filename(slug: str, version: int = 0, extension: str = ".py") -> str:
    """
    Convert problem slug to filename
    
    Args:
        slug: Problem slug (e.g., "two-sum")
        version: Version number (0 for single version)
        extension: File extension
        
    Returns:
        Formatted filename
    """
    base_name = sanitize_filename(slug)
    
    if version > 0:
        return f"{base_name}_v{version}{extension}"
    return f"{base_name}{extension}"


def format_tags(tags: List[str]) -> str:
    """
    Format tags as comma-separated string
    
    Args:
        tags: List of tags
        
    Returns:
        Formatted string
    """
    return ", ".join(tags)


def parse_date_range_choice(choice: str) -> int:
    """
    Parse user's date range choice into days
    
    Args:
        choice: User input
        
    Returns:
        Number of days (-1 for all time)
    """
    choice = choice.strip().lower()
    
    if choice in ['5', 'all', 'all time']:
        return -1
    elif choice in ['1', '7']:
        return 7
    elif choice in ['2', '30']:
        return 30
    elif choice in ['3', '60']:
        return 60
    elif choice in ['4', '90']:
        return 90
    else:
        # Try to parse as integer
        try:
            return int(choice)
        except ValueError:
            return 30  # Default to 30 days


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to max length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_runtime(runtime: str) -> str:
    """Format runtime string"""
    if not runtime or runtime == "N/A":
        return "N/A"
    return runtime


def format_memory(memory: str) -> str:
    """Format memory string"""
    if not memory or memory == "N/A":
        return "N/A"
    return memory
