"""
All enums used across the project
Clean, centralized, easy to maintain
"""
from enum import Enum


class SubmissionStatus(Enum):
    """Submission status from LeetCode"""
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded"
    RUNTIME_ERROR = "Runtime Error"
    COMPILE_ERROR = "Compile Error"
    PENDING = "Pending"


class Difficulty(Enum):
    """Problem difficulty levels"""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    PYTHON3 = "python3"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUBY = "ruby"
    SWIFT = "swift"
    GOLANG = "golang"
    SCALA = "scala"
    KOTLIN = "kotlin"
    RUST = "rust"
    PHP = "php"
    MYSQL = "mysql"
    MSSQL = "mssql"
    ORACLESQL = "oraclesql"
    POSTGRESQL = "postgresql"


class FileExtension(Enum):
    """File extensions by language"""
    PYTHON = ".py"
    PYTHON3 = ".py"
    JAVA = ".java"
    CPP = ".cpp"
    C = ".c"
    CSHARP = ".cs"
    JAVASCRIPT = ".js"
    TYPESCRIPT = ".ts"
    RUBY = ".rb"
    SWIFT = ".swift"
    GOLANG = ".go"
    SCALA = ".scala"
    KOTLIN = ".kt"
    RUST = ".rs"
    PHP = ".php"
    MYSQL = ".sql"
    MSSQL = ".sql"
    ORACLESQL = ".sql"
    POSTGRESQL = ".sql"


class SyncMode(Enum):
    """Sync operation modes"""
    FULL = "full"  # Sync all matching submissions
    INCREMENTAL = "incremental"  # Only new submissions
    UPDATE = "update"  # Update existing files


class VersionNaming(Enum):
    """Version naming strategies for multiple solutions"""
    SEQUENTIAL = "sequential"  # v1, v2, v3
    TIMESTAMP = "timestamp"  # 20241004_120000
    DATETIME = "datetime"  # 2024-10-04_12-00-00


class MultiTagBehavior(Enum):
    """How to handle problems with multiple tags"""
    PRIMARY = "primary"  # Use first matching tag
    ALL = "all"  # Save in all matching folders
    FIRST = "first"  # Use first tag found


class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class GitHubCommitType(Enum):
    """Types of commits"""
    ADD = "Add"
    UPDATE = "Update"
    SYNC = "Sync"
    REFACTOR = "Refactor"
