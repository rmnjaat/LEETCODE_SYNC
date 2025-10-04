# 🚀 LeetCode to GitHub Sync

Automatically fetch your LeetCode submissions and sync them to GitHub, organized by tags!

## ✨ Features

- 🔄 **Automatic Sync**: Fetch submissions directly from LeetCode's API
- 🏷️ **Tag-Based Organization**: Organize solutions by problem tags (Database, Array, Tree, etc.)
- 📚 **Multiple Solutions**: Keep all versions of your solutions with version numbering
- 🎯 **Flexible Configuration**: Easy YAML configuration for tags and folders
- 📅 **Date Range Selection**: Sync last 7, 30, 60, 90 days or all time
- 💾 **Complete Code**: Full submission code with metadata (difficulty, runtime, tags)
- 🧹 **Clean Architecture**: Well-organized, maintainable codebase

## 📋 Prerequisites

- Python 3.8 or higher
- LeetCode account
- GitHub account
- GitHub Personal Access Token

## 🛠️ Installation

### 1. Clone or Download

```bash
cd "Leetcode project"
```

### 2. Create Conda Environment

```bash
conda create -n leetcode-project python=3.10 -y
conda activate leetcode-project
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Setup Environment Variables

Copy `env.example` to `.env`:

```bash
cp env.example .env
```

Edit `.env` and add your credentials:

```env
# Get from browser after logging into LeetCode
LEETCODE_SESSION=your_session_cookie_here
LEETCODE_CSRF_TOKEN=your_csrf_token_here

# Generate from GitHub Settings -> Developer Settings -> Personal Access Tokens
GITHUB_TOKEN=your_github_token_here
```

#### 📖 Detailed Credentials Guide

**Need help getting these credentials?** We have comprehensive guides:

- 📄 **[CREDENTIALS_GUIDE.md](CREDENTIALS_GUIDE.md)** - Complete step-by-step guide with detailed instructions
- 📄 **[QUICK_REFERENCE_CREDENTIALS.txt](QUICK_REFERENCE_CREDENTIALS.txt)** - Quick reference card (print this!)
- 📄 **[env.example](env.example)** - Template with inline instructions

#### Quick Instructions:

**LeetCode Cookies:**
1. Login to [leetcode.com](https://leetcode.com)
2. Press `F12` (Developer Tools)
3. Go to **Application** → **Cookies** → `https://leetcode.com`
4. Copy: `LEETCODE_SESSION` and `csrftoken` values

**GitHub Token:**
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Generate new token (classic)
3. Check scope: ✅ `repo`
4. Generate and copy token

> 💡 **Tip:** See `CREDENTIALS_GUIDE.md` for browser-specific instructions and screenshots descriptions!

### 2. Configure Application Settings

Edit `config/config.yaml`:

```yaml
leetcode:
  username: "your_leetcode_username"  # Your LeetCode username

github:
  username: "your_github_username"    # Your GitHub username
  repository: "leetcode-solutions"    # Repository name
  branch: "main"

sync_settings:
  days_to_look_back: 30              # Default days
  only_accepted: true                # Only sync accepted submissions
  keep_all_versions: true            # Keep multiple solutions
```

### 3. Configure Tags

Edit `config/tag_mappings.yaml`:

```yaml
# Which tags to sync (add more as needed)
active_tags:
  - "Database"   # Currently active
  # - "Array"    # Uncomment to enable
  # - "Tree"

# Folder names for each tag
tag_mappings:
  Database: "Databases"
  Array: "Arrays"
  Tree: "Trees"
  # Add more as needed...
```

## 🚀 Usage

### Run the Sync

```bash
conda activate leetcode-project
python main.py
```

### Interactive Prompts

The script will ask you:

1. **Date range**: How many days back to fetch?
   - Last 7 days
   - Last 30 days
   - Last 60 days
   - Last 90 days
   - All time

2. **Confirmation**: Review settings and confirm

### Example Output

```
============================================================
  LeetCode to GitHub Sync
  Automatically sync your LeetCode solutions to GitHub
============================================================

Testing connections...
✓ LeetCode connection test successful
✓ GitHub connection test successful

How many days back should I fetch submissions?
  [1] Last 7 days
  [2] Last 30 days
  [3] Last 60 days
  [4] Last 90 days
  [5] All time

Enter your choice [1-5] (default: 2): 2

Configuration:
  LeetCode User: your_username
  GitHub Repo: your_username/leetcode-solutions
  Active Tags: Database
  Date Range: Last 30 days

Proceed with sync? [Y/n]: y

============================================================
Starting LeetCode to GitHub sync...
============================================================
✓ Found 45 total submissions
✓ Filtered to 12 Database-tagged problems
✓ Organized into 15 files

Uploading to GitHub...
✓ Created file: Databases/combine-two-tables_v1.sql
✓ Created file: Databases/combine-two-tables_v2.sql
...

============================================================
Sync completed!
✓ Files created/updated: 15
  Skipped: 0
  Errors: 0
✓ Repository: https://github.com/your_username/leetcode-solutions
============================================================
```

## 📂 Output Structure

Your GitHub repository will look like:

```
leetcode-solutions/
├── Databases/
│   ├── combine-two-tables_v1.sql
│   ├── combine-two-tables_v2.sql      # Multiple solutions kept!
│   ├── second-highest-salary.sql
│   ├── nth-highest-salary_v1.sql
│   └── ...
├── Arrays/                             # When you enable Array tag
│   ├── two-sum_v1.py
│   └── ...
└── README.md
```

### Solution File Format

Each file includes:

```sql
-- Problem: 175. Combine Two Tables
-- Link: https://leetcode.com/problems/combine-two-tables/
-- Difficulty: Easy
-- Tags: Database
-- Submitted: 2024-10-04 14:30:22
-- Status: Accepted

-- Your solution code here
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

## 🎯 Features Explained

### Multiple Solutions

When you solve the same problem multiple times, all versions are kept:

```
combine-two-tables_v1.sql  ← First attempt
combine-two-tables_v2.sql  ← Improved solution
combine-two-tables_v3.sql  ← Optimized version
```

### Flexible Tag Mapping

Easily add more tags without touching code:

```yaml
active_tags:
  - "Database"
  - "Array"           # Just add here!
  - "Dynamic Programming"
```

## 🔧 Advanced Usage

### Sync Specific Date Range

Modify `days_to_look_back` in `config/config.yaml` to change the default.

### Add More Tags

1. Edit `config/tag_mappings.yaml`
2. Add tag to `active_tags` list
3. Run sync again

### Change Folder Names

Edit the `tag_mappings` in `config/tag_mappings.yaml`:

```yaml
tag_mappings:
  Database: "SQL-Problems"    # Custom folder name
  Array: "Array-Solutions"
```

## 📝 Project Structure

```
leetcode-github-sync/
├── src/
│   ├── core/              # API clients
│   │   ├── leetcode_client.py
│   │   └── github_client.py
│   ├── services/          # Business logic
│   │   ├── sync_service.py
│   │   ├── solution_organizer.py
│   │   └── file_formatter.py
│   ├── models/            # Data models
│   │   ├── submission.py
│   │   ├── problem.py
│   │   └── sync_result.py
│   ├── config/            # Configuration & enums
│   │   ├── enums.py
│   │   ├── constants.py
│   │   └── settings.py
│   └── utils/             # Utilities
│       ├── logger.py
│       └── helpers.py
├── config/                # YAML configs
│   ├── config.yaml
│   └── tag_mappings.yaml
├── logs/                  # Log files
├── main.py               # Entry point
└── requirements.txt
```

## 🐛 Troubleshooting

### "LEETCODE_SESSION not set"

- Make sure you copied `env.example` to `.env`
- Verify the session cookie is correct and not expired
- Try logging out and back into LeetCode to get fresh cookie

### "Failed to connect to repository"

- Check GitHub token has `repo` scope
- Verify repository name is correct
- Make sure repository exists (or create it)

### "No submissions found"

- Check LeetCode username is correct
- Verify session cookie is valid
- Try increasing the date range

### Connection Test Fails

- Check your internet connection
- Verify credentials are correct and not expired
- Check if LeetCode/GitHub is accessible

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## 📧 Support

If you encounter issues:
1. Check the logs in `logs/sync.log`
2. Verify your configuration
3. Ensure credentials are valid

## 🎉 Acknowledgments

Built with:
- LeetCode GraphQL API
- PyGithub
- Python 3

---

**Happy coding!** 🚀
