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

# GraphQL Queries
GRAPHQL_RECENT_SUBMISSIONS = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

GRAPHQL_SUBMISSION_DETAIL = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    id
    code
    timestamp
    lang {
      name
    }
    runtimeDisplay
    memoryDisplay
    question {
      questionId
      title
      titleSlug
      content
      difficulty
      topicTags {
        name
      }
    }
  }
}
"""

GRAPHQL_QUESTION_DETAIL = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    content
    difficulty
    topicTags {
      name
      slug
    }
  }
}
"""
