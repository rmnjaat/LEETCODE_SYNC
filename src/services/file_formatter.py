"""
File formatter service
Formats solution files with metadata
"""
from typing import Optional
from src.models.submission import Submission
from src.config.constants import FILE_HEADER_TEMPLATE, SQL_COMMENT_TEMPLATE
from src.utils.helpers import format_tags, format_runtime, format_memory


class FileFormatter:
    """Formats solution files with metadata"""
    
    @staticmethod
    def format_solution_file(submission: Submission, version: Optional[int] = None) -> str:
        """
        Format a complete solution file with metadata and code
        
        Args:
            submission: Submission object
            version: Optional version number
            
        Returns:
            Formatted file content
        """
        problem = submission.problem
        
        # Version info
        version_info = ""
        if version:
            version_info = f" * - Version: {version}\n"
        
        # Choose template based on language
        is_sql = submission.language.lower() in ['mysql', 'mssql', 'oraclesql', 'postgresql']
        
        if is_sql:
            header = SQL_COMMENT_TEMPLATE.format(
                problem_id=problem.question_id,
                title=problem.title,
                url=problem.url,
                difficulty=problem.difficulty,
                tags=format_tags(problem.tags),
                timestamp=submission.formatted_timestamp,
                status=submission.status
            )
        else:
            header = FILE_HEADER_TEMPLATE.format(
                problem_id=problem.question_id,
                title=problem.title,
                url=problem.url,
                difficulty=problem.difficulty,
                tags=format_tags(problem.tags),
                timestamp=submission.formatted_timestamp,
                status=submission.status,
                runtime=format_runtime(submission.runtime),
                memory=format_memory(submission.memory),
                language=submission.language,
                version_info=version_info
            )
        
        # Combine header and code
        content = header + "\n" + submission.code
        
        return content
    
    @staticmethod
    def format_readme_section(tag: str, problems: list, stats: dict) -> str:
        """
        Format a README section for a tag
        
        Args:
            tag: Tag name
            problems: List of problems
            stats: Statistics dictionary
            
        Returns:
            Formatted README section
        """
        section = f"\n## {tag}\n\n"
        section += f"**Total Problems:** {len(problems)}\n\n"
        
        if problems:
            section += "| # | Problem | Difficulty | Solutions |\n"
            section += "|---|---------|------------|-----------|\n"
            
            for prob in problems:
                section += f"| {prob['id']} | [{prob['title']}]({prob['url']}) | {prob['difficulty']} | {prob['solutions']} |\n"
        
        return section
