# LeetCode to GitHub Sync - Detailed Implementation Plan

## 🎯 Project Requirements
- Fetch submissions from LeetCode account
- Organize by tags (starting with "Databases" tag)
- Push solutions to GitHub repository
- Allow user to specify: number of days to look back for submissions
- Handle multiple solutions for the same problem (keep all versions)
- Display the actual code submitted

---

## 📊 How We'll Get Data from LeetCode

### Method: LeetCode GraphQL API

**API Endpoint:** `https://leetcode.com/graphql`

### Authentication Process:
1. **Get Session Cookie:**
   - Login to LeetCode in your browser
   - Open Developer Tools (F12)
   - Go to Application/Storage → Cookies → https://leetcode.com
   - Copy the `LEETCODE_SESSION` cookie value
   - Store it in `.env` file

2. **API Authentication:**
   - Include the session cookie in request headers:
   ```
   Cookie: LEETCODE_SESSION=your_session_value
   csrftoken: your_csrf_token
   ```

### GraphQL Queries We'll Use:

#### 1. Get User's Accepted Submissions List
```graphql
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
    lang
  }
}
```

#### 2. Get Full Submission Code
```graphql
query submissionDetails($submissionId: Int!) {
  submissionDetail(submissionId: $submissionId) {
    id
    code
    timestamp
    statusDisplay
    lang
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
```

#### 3. Get Problem Details with Tags
```graphql
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
    sampleTestCase
    exampleTestcases
  }
}
```

---

## 🔄 Data Fetching Workflow

```
1. User Inputs:
   ├─ LeetCode Username
   ├─ Number of days to look back (e.g., 30, 60, 90, or "all")
   ├─ GitHub repository details
   └─ Tag filter (e.g., "Databases")

2. Fetch All Submissions:
   ├─ Query recentAcSubmissions with large limit (e.g., 200)
   ├─ Filter by timestamp (last N days)
   └─ Get list of submission IDs

3. For Each Submission:
   ├─ Get full submission details (code + problem info)
   ├─ Extract problem tags
   ├─ Check if "Databases" tag exists
   └─ If matched, add to processing queue

4. Handle Multiple Solutions:
   ├─ Group submissions by problem title/slug
   ├─ If multiple solutions exist for same problem:
   │   ├─ Keep all versions
   │   ├─ Name with timestamps: problem-name_20241004_120000.sql
   │   ├─ Or version numbers: problem-name_v1.sql, problem-name_v2.sql
   │   └─ Add metadata comment showing submission date
   └─ Store each version separately

5. Format Solution Files:
   ├─ Add header comment with metadata
   ├─ Include problem link, difficulty, tags
   ├─ Add problem description
   └─ Include the actual submitted code

6. Push to GitHub:
   ├─ Create/Update files in Databases/ folder
   ├─ Commit with descriptive message
   └─ Push to repository
```

---

## 🗂️ Repository Structure

```
leetcode-solutions/
├── Databases/
│   ├── combine-two-tables_v1.sql
│   ├── combine-two-tables_v2.sql        # Multiple solutions kept
│   ├── second-highest-salary.sql
│   ├── nth-highest-salary.sql
│   └── ...
├── README.md                             # Auto-generated index
└── .github/
    └── last_sync.json                    # Track sync status
```

---

## 📝 Solution File Format

Each solution file will look like:
```sql
/*
 * Problem: 175. Combine Two Tables
 * Link: https://leetcode.com/problems/combine-two-tables/
 * Difficulty: Easy
 * Tags: Database
 * Submitted: 2024-10-04 12:30:45
 * Status: Accepted
 * 
 * Problem Description:
 * [Problem description here]
 */

-- Solution Code:
SELECT 
    p.firstName, 
    p.lastName, 
    a.city, 
    a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

---

## 🛠️ Technical Implementation

### Python Libraries Needed:
```
requests          # HTTP requests to LeetCode API
PyGithub          # GitHub API interaction
python-dotenv     # Environment variables
pyyaml            # Configuration files
```

### Project File Structure:
```
leetcode-github-sync/
├── src/
│   ├── __init__.py
│   ├── leetcode_client.py       # LeetCode API client
│   ├── github_client.py         # GitHub API client
│   ├── organizer.py             # Organize solutions by tags
│   ├── formatter.py             # Format solution files
│   └── main.py                  # Main orchestration
├── config/
│   └── config.yaml              # User configuration
├── .env                         # Secrets (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔐 Configuration Files

### `.env` (Secret - Not Committed)
```
LEETCODE_SESSION=your_session_cookie_here
LEETCODE_CSRF_TOKEN=your_csrf_token_here
GITHUB_TOKEN=your_github_personal_access_token
```

### `config/config.yaml`
```yaml
leetcode:
  username: "your_leetcode_username"
  
github:
  username: "your_github_username"
  repository: "leetcode-solutions"
  
sync_settings:
  days_to_look_back: 30           # User can change this
  tags_to_sync:
    - "Database"                  # Starting with Databases
  keep_all_versions: true         # Keep multiple solutions
  only_accepted: true             # Only sync accepted submissions
```

---

## 🎮 User Experience Flow

```bash
$ python main.py

=== LeetCode to GitHub Sync ===

1. How many days back to fetch submissions?
   Options: [7, 30, 60, 90, all]
   Enter: 30

2. Fetching submissions from last 30 days...
   ✓ Found 45 total submissions
   ✓ Filtered to 12 'Database' tagged problems
   ✓ Detected 3 problems with multiple solutions

3. Processing submissions:
   [1/12] Combine Two Tables (2 versions found)
   [2/12] Second Highest Salary (1 version)
   ...

4. Multiple solutions detected:
   - "Combine Two Tables": 2 solutions found
     Keep all versions? [Y/n]: Y
     
5. Uploading to GitHub...
   ✓ Created/Updated 14 files
   ✓ Committed: "Sync: 14 Database solutions (2024-10-04)"
   ✓ Pushed to github.com/username/leetcode-solutions

✅ Sync completed successfully!
```

---

## 🔍 Key Features

### 1. Date Range Selection
- User prompted at runtime OR set in config
- Calculate timestamp: `current_time - (days * 24 * 3600)`
- Filter submissions where `timestamp >= cutoff_timestamp`

### 2. Multiple Solutions Handling
**When multiple solutions exist for same problem:**

**Option A: Timestamp-based naming**
```
problem-name_20241001_143022.sql
problem-name_20241004_120045.sql
```

**Option B: Version-based naming (Sequential)**
```
problem-name_v1.sql
problem-name_v2.sql
```

**Each file includes:**
- Submission timestamp in header
- Status (Accepted, Runtime, Memory usage if available)
- Original code exactly as submitted

### 3. Tag Filtering
- Fetch problem tags from API
- Check if "Database" in `topicTags`
- Only process matched problems
- Easy to extend to multiple tags later

---

## 📈 Future Enhancements
- Multiple tag support (Arrays, Trees, etc.)
- Separate repos per tag
- Auto-generate README with statistics
- Schedule automatic syncs (cron/GitHub Actions)
- Compare solutions (show improvements)
- Add test cases to files

---

## 🚀 Next Steps

1. **Setup Phase:**
   - Create project structure
   - Install dependencies
   - Setup .env file with credentials

2. **Development Phase:**
   - Implement LeetCode API client
   - Test fetching submissions
   - Implement GitHub uploader
   - Add formatting logic

3. **Testing Phase:**
   - Test with your account
   - Verify multiple solution handling
   - Test date filtering

4. **Deployment:**
   - Run and sync your solutions
   - Verify GitHub repository

---

## ❓ Questions Answered

### Q: How will you get data from LeetCode?
**A:** Using LeetCode's official GraphQL API at `https://leetcode.com/graphql` with your session cookie for authentication. We'll query:
1. List of recent submissions
2. Full submission details (code, timestamps)
3. Problem details (tags, difficulty, description)

### Q: What if multiple solutions for one question exist?
**A:** We'll keep ALL of them! Each solution will be saved with either:
- Timestamp suffix: `problem_20241004_120000.sql`
- Version number: `problem_v1.sql`, `problem_v2.sql`

### Q: How many days to look back?
**A:** User will be prompted at runtime to enter: 7, 30, 60, 90 days, or "all". This filters submissions by timestamp.

### Q: Tags?
**A:** Starting with "Databases" tag only. We'll fetch problem tags from API and only process problems tagged with "Database".

---

**Ready to implement?** 🚀
