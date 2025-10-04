# 🔄 Data Flow: How We Get LeetCode Submissions

## Simple Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR LEETCODE ACCOUNT                         │
│                  (leetcode.com/username)                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 1. Authenticate with Session Cookie
                      │    (LEETCODE_SESSION from browser)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              LEETCODE GraphQL API                                │
│              https://leetcode.com/graphql                        │
│                                                                  │
│  Available Queries:                                              │
│  • recentAcSubmissionList → Get list of submissions             │
│  • submissionDetail → Get specific submission code              │
│  • question → Get problem details & tags                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 2. Fetch Data via HTTP POST Requests
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUR PYTHON SCRIPT                             │
│                                                                  │
│  Step 1: Get all submissions (last N days)                      │
│  ├─ Query: recentAcSubmissionList                               │
│  ├─ Filter by timestamp (last 30/60/90 days)                    │
│  └─ Result: List of submission IDs                              │
│                                                                  │
│  Step 2: For each submission ID, get full details               │
│  ├─ Query: submissionDetail                                     │
│  ├─ Extract: code, language, timestamp, problem info            │
│  └─ Result: Full submission with code                           │
│                                                                  │
│  Step 3: Get problem tags                                       │
│  ├─ Already in submissionDetail response                        │
│  ├─ Check if "Database" tag exists                              │
│  └─ Filter: Only keep Database problems                         │
│                                                                  │
│  Step 4: Handle Multiple Solutions                              │
│  ├─ Group by problem slug/title                                 │
│  ├─ If problem has multiple submissions:                        │
│  │   ├─ Sort by timestamp                                       │
│  │   └─ Name: problem_v1.sql, problem_v2.sql, etc.             │
│  └─ Keep ALL versions (as requested)                            │
│                                                                  │
│  Step 5: Format each solution                                   │
│  ├─ Add header with problem info                                │
│  ├─ Add link, difficulty, tags                                  │
│  ├─ Add problem description                                     │
│  └─ Add the actual code submitted                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 3. Upload via GitHub API
                      │    (Using PyGithub library)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR GITHUB REPOSITORY                        │
│                  github.com/username/leetcode-solutions          │
│                                                                  │
│  Databases/                                                      │
│  ├── combine-two-tables_v1.sql                                  │
│  ├── combine-two-tables_v2.sql    ← Multiple solutions!         │
│  ├── second-highest-salary.sql                                  │
│  └── ...                                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Detailed: How LeetCode API Works

### Method 1: Get Submission List
**What we send:**
```python
import requests

url = "https://leetcode.com/graphql"
headers = {
    "Cookie": "LEETCODE_SESSION=your_cookie_here",
    "Content-Type": "application/json"
}

query = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
    lang
  }
}
"""

variables = {
    "username": "your_username",
    "limit": 100
}

response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
data = response.json()
```

**What we get back:**
```json
{
  "data": {
    "recentAcSubmissionList": [
      {
        "id": "1234567890",
        "title": "Combine Two Tables",
        "titleSlug": "combine-two-tables",
        "timestamp": "1696435200",
        "lang": "mysql"
      },
      {
        "id": "1234567891",
        "title": "Second Highest Salary",
        "titleSlug": "second-highest-salary",
        "timestamp": "1696521600",
        "lang": "mysql"
      }
      // ... more submissions
    ]
  }
}
```

---

### Method 2: Get Full Submission Code
**For each submission ID from above:**
```python
query = """
query submissionDetails($submissionId: Int!) {
  submissionDetail(submissionId: $submissionId) {
    id
    code
    timestamp
    statusDisplay
    lang
    memory
    runtime
    question {
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
}
"""

variables = {
    "submissionId": 1234567890
}

response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
```

**What we get back:**
```json
{
  "data": {
    "submissionDetail": {
      "id": "1234567890",
      "code": "SELECT p.firstName, p.lastName, a.city, a.state\nFROM Person p\nLEFT JOIN Address a ON p.personId = a.personId;",
      "timestamp": "1696435200",
      "statusDisplay": "Accepted",
      "lang": "mysql",
      "memory": "0",
      "runtime": "456",
      "question": {
        "questionId": "175",
        "title": "Combine Two Tables",
        "titleSlug": "combine-two-tables",
        "content": "<p>Table: Person...</p>",
        "difficulty": "Easy",
        "topicTags": [
          {
            "name": "Database",
            "slug": "database"
          }
        ]
      }
    }
  }
}
```

---

## 🎯 Key Points

### 1. Authentication
- **Where to get cookie:**
  1. Login to leetcode.com
  2. Press F12 (Developer Tools)
  3. Go to "Application" or "Storage" tab
  4. Click "Cookies" → "https://leetcode.com"
  5. Find `LEETCODE_SESSION`
  6. Copy the value

- **How we use it:**
  ```python
  headers = {
      "Cookie": f"LEETCODE_SESSION={your_session}"
  }
  ```

### 2. Date Filtering
```python
from datetime import datetime, timedelta

# User wants last 30 days
days_back = 30
cutoff_timestamp = int((datetime.now() - timedelta(days=days_back)).timestamp())

# Filter submissions
filtered = [sub for sub in all_submissions 
            if int(sub['timestamp']) >= cutoff_timestamp]
```

### 3. Multiple Solutions Handling

**Scenario:** You solved "Combine Two Tables" on:
- Oct 1, 2024 (first attempt)
- Oct 4, 2024 (improved solution)

**What we do:**
```python
submissions_by_problem = {}

for submission in all_submissions:
    problem_slug = submission['titleSlug']
    
    if problem_slug not in submissions_by_problem:
        submissions_by_problem[problem_slug] = []
    
    submissions_by_problem[problem_slug].append(submission)

# For "combine-two-tables": 2 submissions found
# Save as:
#   - combine-two-tables_v1.sql (Oct 1)
#   - combine-two-tables_v2.sql (Oct 4)

for problem_slug, submissions in submissions_by_problem.items():
    # Sort by timestamp
    submissions.sort(key=lambda x: x['timestamp'])
    
    for idx, submission in enumerate(submissions, 1):
        filename = f"{problem_slug}_v{idx}.sql"
        # Save with full code and metadata
```

### 4. Tag Filtering

```python
# Only keep problems with "Database" tag
database_submissions = []

for submission in all_submissions:
    tags = submission['question']['topicTags']
    tag_names = [tag['name'].lower() for tag in tags]
    
    if 'database' in tag_names:
        database_submissions.append(submission)
```

---

## 📊 Example Run

```
User runs: python main.py

Script asks: "How many days back? [7/30/60/90/all]"
User enters: 30

What happens:
1. Calculate cutoff: Oct 4, 2024 - 30 days = Sep 4, 2024
2. Fetch all submissions from LeetCode API
3. Filter: Keep only submissions after Sep 4, 2024
4. Result: 45 total submissions

5. For each submission:
   - Get full code via API
   - Check tags
   - Filter: 12 have "Database" tag

6. Group by problem:
   - "combine-two-tables": 2 submissions found
   - "second-highest-salary": 1 submission found
   - "nth-highest-salary": 3 submissions found
   - ... 9 more problems

7. Ask user: "Keep all versions? [Y/n]"
   User: Y

8. Create files:
   Databases/
   ├── combine-two-tables_v1.sql
   ├── combine-two-tables_v2.sql
   ├── second-highest-salary.sql
   ├── nth-highest-salary_v1.sql
   ├── nth-highest-salary_v2.sql
   ├── nth-highest-salary_v3.sql
   └── ... (total 15 files)

9. Upload to GitHub
10. Done! ✓
```

---

## 🔒 Security Notes

**What gets stored where:**

```
.env (NEVER commit to Git!)
├── LEETCODE_SESSION=your_cookie
└── GITHUB_TOKEN=your_token

config.yaml (Safe to commit)
├── username: "ramanjangu"
├── days_to_look_back: 30
└── tags: ["Database"]

.gitignore (MUST include)
├── .env
├── __pycache__/
└── *.pyc
```

---

## ✅ Summary

**Data Source:** LeetCode GraphQL API  
**Authentication:** Session cookie from browser  
**Data Retrieved:** Submission code, timestamps, problem details, tags  
**Filtering:** By date range + "Database" tag  
**Multiple Solutions:** Keep all versions with v1, v2, v3... naming  
**Destination:** GitHub repository in Databases/ folder  

**This is a fully automated, reliable method that uses LeetCode's official API!**
