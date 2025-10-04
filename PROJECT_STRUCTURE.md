# 📁 Project Structure - Clean & Flexible

## Complete Folder Structure

```
leetcode-github-sync/
│
├── 📂 src/
│   ├── __init__.py
│   │
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── leetcode_client.py      # LeetCode API client
│   │   ├── github_client.py        # GitHub API client
│   │   └── file_formatter.py       # Format solution files
│   │
│   ├── 📂 services/
│   │   ├── __init__.py
│   │   ├── submission_fetcher.py   # Fetch & filter submissions
│   │   ├── solution_organizer.py   # Organize by tags
│   │   └── sync_service.py         # Main sync orchestration
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── submission.py           # Submission data class
│   │   ├── problem.py              # Problem data class
│   │   └── sync_result.py          # Sync result data class
│   │
│   ├── 📂 config/
│   │   ├── __init__.py
│   │   ├── settings.py             # Load configuration
│   │   ├── enums.py                # All enums here
│   │   └── constants.py            # Constants
│   │
│   └── 📂 utils/
│       ├── __init__.py
│       ├── logger.py               # Logging utilities
│       ├── validators.py           # Input validation
│       └── helpers.py              # Helper functions
│
├── 📂 config/
│   ├── config.yaml                 # Main configuration
│   ├── tag_mappings.yaml           # Tag-to-folder mappings (flexible!)
│   └── config.example.yaml         # Example config (for GitHub)
│
├── 📂 tests/
│   ├── __init__.py
│   ├── test_leetcode_client.py
│   ├── test_github_client.py
│   └── test_organizer.py
│
├── 📂 logs/
│   └── sync.log                    # Auto-generated logs
│
├── .env                            # Secrets (NOT committed)
├── .env.example                    # Template for .env
├── .gitignore
├── requirements.txt
├── setup.py                        # Package setup
├── main.py                         # Entry point
└── README.md
```

---

## 🎯 Flexible Tag-to-Folder Mapping

### Configuration File: `config/tag_mappings.yaml`

```yaml
# Flexible tag to folder/repository mapping
# Change this anytime without touching code!

tag_mappings:
  # LeetCode Tag Name : GitHub Folder Name
  Database: "Databases"
  Array: "Arrays"
  String: "Strings"
  "Dynamic Programming": "Dynamic-Programming"
  Tree: "Trees"
  Graph: "Graphs"
  "Linked List": "Linked-Lists"
  "Binary Search": "Binary-Search"
  "Depth-First Search": "DFS"
  "Breadth-First Search": "BFS"
  Backtracking: "Backtracking"
  Greedy: "Greedy"
  "Two Pointers": "Two-Pointers"
  Math: "Math"
  "Bit Manipulation": "Bit-Manipulation"
  Heap: "Heaps"
  Stack: "Stacks"
  Queue: "Queues"
  Design: "System-Design"

# Tags to sync (only these will be processed)
active_tags:
  - "Database"  # Start with only Database
  # - "Array"   # Uncomment to add more
  # - "Tree"

# Behavior when problem has multiple tags
multi_tag_behavior: "primary"  # Options: "primary", "all", "first"
# primary: Use first tag from active_tags
# all: Save in all matching folders
# first: Use first tag found

# Default folder for unmatched tags
default_folder: "Others"
```

### Main Config: `config/config.yaml`

```yaml
leetcode:
  username: "your_leetcode_username"
  base_url: "https://leetcode.com"
  api_endpoint: "https://leetcode.com/graphql"

github:
  username: "your_github_username"
  repository: "leetcode-solutions"
  branch: "main"
  base_path: ""  # Root of repo, or "solutions/" for subfolder

sync_settings:
  days_to_look_back: 30
  only_accepted: true
  keep_all_versions: true
  version_naming: "sequential"  # Options: "sequential", "timestamp"
  
  # File naming patterns
  file_patterns:
    sequential: "{problem_slug}_v{version}.{ext}"
    timestamp: "{problem_slug}_{timestamp}.{ext}"
    single: "{problem_slug}.{ext}"

  # Filters
  filters:
    status: ["Accepted"]  # Can add: "Wrong Answer", etc.
    languages: []  # Empty = all, or ["mysql", "python3"]

  # README generation
  generate_readme: true
  readme_template: "default"  # Or custom path

logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "logs/sync.log"
  console: true
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 📦 Enums File: `src/config/enums.py`

```python
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
```

---

## 🏗️ Constants File: `src/config/constants.py`

```python
"""
Application constants
Centralized, easy to modify
"""

# LeetCode API
LEETCODE_GRAPHQL_ENDPOINT = "https://leetcode.com/graphql"
LEETCODE_BASE_URL = "https://leetcode.com"
LEETCODE_PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/{slug}/"

# Default values
DEFAULT_SUBMISSION_LIMIT = 200
DEFAULT_DAYS_BACK = 30
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 2  # seconds

# Rate limiting
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_PERIOD = 60  # seconds

# File headers
FILE_HEADER_TEMPLATE = """/*
 * Problem: {problem_id}. {title}
 * Link: {url}
 * Difficulty: {difficulty}
 * Tags: {tags}
 * 
 * Submission Info:
 * - Submitted: {timestamp}
 * - Status: {status}
 * - Runtime: {runtime}
 * - Memory: {memory}
 * - Language: {language}
 * {version_info}
 */

"""

SQL_COMMENT_TEMPLATE = """-- Problem: {problem_id}. {title}
-- Link: {url}
-- Difficulty: {difficulty}
-- Tags: {tags}
-- Submitted: {timestamp}
-- Status: {status}

"""

# Commit messages
COMMIT_MESSAGES = {
    "add": "Add: {problem_title} solution",
    "update": "Update: {problem_title} solution (v{version})",
    "sync": "Sync: {count} {tag} solutions",
    "bulk": "Sync: {count} solutions across {tag_count} categories"
}

# README templates
README_HEADER = """# LeetCode Solutions

Auto-synced from LeetCode account.

## Statistics

- **Total Problems Solved:** {total}
- **Easy:** {easy} | **Medium:** {medium} | **Hard:** {hard}
- **Last Updated:** {date}

---

"""

# Validation
MAX_FILENAME_LENGTH = 200
INVALID_FILENAME_CHARS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

# GitHub
GITHUB_API_BASE = "https://api.github.com"
MAX_COMMIT_MESSAGE_LENGTH = 72
```

---

## 📊 Example of Clean Separation

### Data Models: `src/models/submission.py`

```python
"""
Submission data model
Clean, typed, reusable
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.config.enums import SubmissionStatus, Difficulty, Language


@dataclass
class Problem:
    """Problem details"""
    question_id: str
    title: str
    title_slug: str
    content: str
    difficulty: Difficulty
    tags: List[str]
    url: str


@dataclass
class Submission:
    """Submission details"""
    id: str
    code: str
    timestamp: datetime
    status: SubmissionStatus
    language: Language
    runtime: Optional[str]
    memory: Optional[str]
    problem: Problem
    
    @property
    def is_accepted(self) -> bool:
        return self.status == SubmissionStatus.ACCEPTED
    
    @property
    def file_extension(self) -> str:
        from src.config.enums import FileExtension
        return FileExtension[self.language.name].value
```

---

## 🎯 GitHub Repository Structure (Your Repo)

After running the sync, your GitHub repo will look like:

```
leetcode-solutions/                    # Your GitHub repository
│
├── Databases/                         # Configured in tag_mappings.yaml
│   ├── combine-two-tables_v1.sql
│   ├── combine-two-tables_v2.sql
│   ├── second-highest-salary.sql
│   ├── nth-highest-salary_v1.sql
│   ├── nth-highest-salary_v2.sql
│   └── ...
│
├── Arrays/                            # When you enable "Array" tag
│   ├── two-sum_v1.py
│   ├── two-sum_v2.py
│   └── ...
│
├── Dynamic-Programming/               # When you enable "Dynamic Programming"
│   ├── climbing-stairs.py
│   └── ...
│
└── README.md                          # Auto-generated
```

---

## 🎨 Benefits of This Structure

### ✅ Clean Code
- **Separation of concerns:** Each module has one job
- **Enums centralized:** Easy to find and modify
- **Models separated:** Clear data structures
- **Config-driven:** No hardcoded values

### ✅ Flexible
- **Tag mappings:** Just edit YAML, no code changes
- **Easy to extend:** Add new tags without touching Python
- **Configurable naming:** Choose version format in config

### ✅ Maintainable
- **Clear structure:** Easy to navigate
- **Type hints:** Better IDE support
- **Documentation:** Each file has clear purpose
- **Testing:** Each component can be tested independently

### ✅ Scalable
- **Add more tags:** Update `tag_mappings.yaml`
- **Change folder names:** Update mapping config
- **Multiple repositories:** Easy to support later

---

## 🔧 How to Add New Tags (No Code Changes!)

**Want to sync "Array" problems too?**

Just edit `config/tag_mappings.yaml`:

```yaml
active_tags:
  - "Database"
  - "Array"      # ← Just add this!
  - "Tree"       # ← And this!
```

Run sync → Automatically creates:
- `Arrays/` folder
- `Trees/` folder

**Want different folder name?**

```yaml
tag_mappings:
  Database: "SQL-Problems"        # ← Custom name!
  Array: "Array-Solutions"        # ← Your choice!
```

---

## 📝 Summary

| Aspect | Location | Flexibility |
|--------|----------|-------------|
| **Enums** | `src/config/enums.py` | Centralized, clean |
| **Constants** | `src/config/constants.py` | Easy to modify |
| **Tag Mappings** | `config/tag_mappings.yaml` | Fully configurable |
| **Settings** | `config/config.yaml` | User-friendly |
| **Business Logic** | `src/services/` | Clean separation |
| **Data Models** | `src/models/` | Type-safe |
| **API Clients** | `src/core/` | Reusable |

---

## 🚀 Next Step

**Should I create this entire structure with all the files?**
- ✅ Clean folder structure
- ✅ Enums file with all enums
- ✅ Config files with flexible mappings
- ✅ Proper Python package structure
- ✅ All the core files

**Ready to build?** 🎯
