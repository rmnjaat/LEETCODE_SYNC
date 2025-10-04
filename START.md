# 🚀 How to Start the Project

## Quick Start Commands

### **Method 1: Using System Python (Recommended)**

```bash
# 1. Navigate to project directory
cd "/Users/ramanjangu/Desktop/Leetcode project"

# 2. Run the application
python3 main.py
```

That's it! The app will:
1. Check if repository exists (auto-create if needed)
2. Test connections
3. Prompt you for options
4. Start syncing

---

### **Method 2: Using Conda Environment**

```bash
# 1. Navigate to project directory
cd "/Users/ramanjangu/Desktop/Leetcode project"

# 2. Activate conda environment
conda activate leetcode-project

# 3. Run the application
python main.py

# 4. When done, deactivate (optional)
conda deactivate
```

---

## 📋 **Complete Workflow**

### **First Time Setup (One Time Only)**

```bash
# 1. Go to project folder
cd "/Users/ramanjangu/Desktop/Leetcode project"

# 2. Create .env file with your credentials
cp env.example .env
nano .env  # or: code .env

# Add your credentials:
#   LEETCODE_SESSION=...
#   LEETCODE_CSRF_TOKEN=...
#   GITHUB_TOKEN=...

# 3. Configure usernames in config.yaml
nano config/config.yaml  # or: code config/config.yaml

# Update:
#   leetcode.username: "your_username"
#   github.username: "your_username"
```

---

### **Every Time You Run**

```bash
# 1. Navigate to project
cd "/Users/ramanjangu/Desktop/Leetcode project"

# 2. Run the sync
python3 main.py

# 3. Follow the prompts:
#    - Repository check (auto-creates if needed)
#    - Connection test (can proceed even if warning)
#    - Choose date range (7/30/60/90 days or all)
#    - Confirm sync
#    - Done!
```

---

## 🎯 **What You'll See**

```bash
$ python3 main.py

============================================================
  LeetCode to GitHub Sync
  Automatically sync your LeetCode solutions to GitHub
============================================================

Checking GitHub repository...
✓ Repository 'leetcode-solutions' found

Testing connections...
✓ LeetCode connection test successful
✓ GitHub connection test successful
✓ All connections successful

How many days back should I fetch submissions?
  [1] Last 7 days
  [2] Last 30 days
  [3] Last 60 days
  [4] Last 90 days
  [5] All time

Enter your choice [1-5] (default: 2): 2

Configuration:
  LeetCode User: rmn_jaat
  GitHub Repo: rmnjaat/leetcode-solutions
  Active Tags: Database
  Date Range: Last 30 days

Proceed with sync? [Y/n]: y

============================================================
Starting LeetCode to GitHub sync...
============================================================
Fetching submissions from last 30 days...
✓ Found 45 total submissions
✓ Filtered to 12 Database-tagged problems
...
```

---

## ⚡ **Quick Reference**

| Command | What It Does |
|---------|--------------|
| `cd "/Users/ramanjangu/Desktop/Leetcode project"` | Go to project folder |
| `python3 main.py` | Run the sync (system Python) |
| `conda activate leetcode-project` | Activate conda env |
| `python main.py` | Run in conda env |
| `nano .env` | Edit credentials |
| `nano config/config.yaml` | Edit configuration |
| `python3 create_repo.py` | Create GitHub repo (optional) |

---

## 🔧 **Troubleshooting**

### If you see: "ModuleNotFoundError"
```bash
pip3 install -r requirements.txt
```

### If you see: "LEETCODE_SESSION not set"
```bash
# Make sure .env file exists
ls -la .env

# Edit it
nano .env
```

### If you see: "Repository not found"
```bash
# The app will ask to create it automatically
# Or create manually at: https://github.com/new
```

### If LeetCode connection fails
```bash
# Get fresh cookies:
# 1. Go to leetcode.com
# 2. Logout and login again
# 3. F12 → Application → Cookies
# 4. Update .env file
```

---

## 📁 **Project Location**

Your project is at:
```
/Users/ramanjangu/Desktop/Leetcode project/
```

**To navigate there from anywhere:**
```bash
cd ~/Desktop/Leetcode\ project
# or
cd "/Users/ramanjangu/Desktop/Leetcode project"
```

---

## 🎨 **Customization**

### Change repository name:
```bash
nano config/config.yaml
# Edit: github.repository: "new-name"
```

### Change tags to sync:
```bash
nano config/tag_mappings.yaml
# Edit: active_tags list
```

### Change date range default:
```bash
nano config/config.yaml
# Edit: sync_settings.days_to_look_back: 30
```

---

## ✅ **Checklist Before Running**

- [ ] `.env` file created with credentials
- [ ] `config/config.yaml` updated with usernames
- [ ] Internet connection active
- [ ] Logged into LeetCode (for fresh cookies)

---

## 🚀 **Ready to Run!**

**Just run this:**
```bash
cd "/Users/ramanjangu/Desktop/Leetcode project" && python3 main.py
```

**That's all!** 🎉
