# 🚀 Quick Setup Guide

## Step-by-Step Setup

### 1. ✅ Conda Environment (Already Done!)

```bash
conda activate leetcode-project
```

### 2. 📝 Configure Your Credentials

#### A. Create .env file

```bash
cp env.example .env
```

#### B. Get LeetCode Credentials

1. **Login to LeetCode**: Go to https://leetcode.com and login
2. **Open DevTools**: Press `F12` or `Right Click → Inspect`
3. **Go to Application Tab**: 
   - Chrome/Edge: `Application` → `Cookies` → `https://leetcode.com`
   - Firefox: `Storage` → `Cookies` → `https://leetcode.com`
4. **Copy These Values**:
   - Find `LEETCODE_SESSION` → Copy the Value
   - Find `csrftoken` → Copy the Value

#### C. Get GitHub Token

1. **Go to GitHub Settings**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Configure**:
   - Note: "LeetCode Sync"
   - Expiration: Choose duration
   - Select scopes: ✅ `repo` (Full control of private repositories)
4. **Generate token** and copy it immediately

#### D. Edit .env File

```bash
# Open .env file
nano .env
# or
code .env
```

Add your values:
```env
LEETCODE_SESSION=your_actual_session_cookie_from_step_B
LEETCODE_CSRF_TOKEN=your_actual_csrf_token_from_step_B
GITHUB_TOKEN=your_actual_github_token_from_step_C
```

**Save and close!**

### 3. ⚙️ Configure Application

Edit `config/config.yaml`:

```bash
nano config/config.yaml
# or
code config/config.yaml
```

Change these values:
```yaml
leetcode:
  username: "your_leetcode_username"  # ← Change this!

github:
  username: "your_github_username"    # ← Change this!
  repository: "leetcode-solutions"    # ← Your repo name
```

**Save!**

### 4. 🏷️ Configure Tags (Optional)

By default, only "Database" tag is active. To add more:

Edit `config/tag_mappings.yaml`:

```yaml
active_tags:
  - "Database"
  # - "Array"           # Uncomment to enable
  # - "Tree"            # Uncomment to enable
```

### 5. 🎯 Create GitHub Repository

**Option A: Let the script create it** (Recommended)
- The script will create the repository automatically on first run

**Option B: Create manually**
1. Go to https://github.com/new
2. Repository name: `leetcode-solutions` (or whatever you set in config)
3. Public or Private: Your choice
4. ✅ Initialize with README
5. Create repository

### 6. 🚀 Run the Sync!

```bash
conda activate leetcode-project
python main.py
```

### 7. 📊 Follow the Prompts

```
How many days back should I fetch submissions?
  [1] Last 7 days
  [2] Last 30 days
  [3] Last 60 days
  [4] Last 90 days
  [5] All time

Enter your choice [1-5] (default: 2): 2
```

### 8. ✅ Check Your GitHub!

After successful sync, visit:
```
https://github.com/YOUR_USERNAME/leetcode-solutions
```

---

## 🔧 Troubleshooting

### Problem: "LEETCODE_SESSION not set"

**Solution**:
- Make sure `.env` file exists (not `env.example`)
- Check that values are not empty
- Try getting fresh cookies from browser

### Problem: "Failed to connect to repository"

**Solution**:
- Verify GitHub token has `repo` scope
- Check repository name matches config
- Make sure token hasn't expired

### Problem: "No submissions found"

**Solution**:
- Verify LeetCode username is correct (case-sensitive!)
- Check if you have solved problems with Database tag
- Try increasing date range to "All time"

### Problem: Session Expired

**Solution**:
- LeetCode sessions expire after some time
- Get fresh `LEETCODE_SESSION` cookie from browser
- Update `.env` file

---

## 📁 Expected Output

After successful sync, your GitHub repo will have:

```
leetcode-solutions/
├── Databases/
│   ├── combine-two-tables_v1.sql
│   ├── combine-two-tables_v2.sql
│   ├── second-highest-salary.sql
│   └── ...
└── README.md
```

Each file contains:
- Problem metadata (title, link, difficulty, tags)
- Submission info (date, status, runtime)
- Your complete solution code

---

## 🎯 Next Steps

1. ✅ Run the sync regularly to keep repository updated
2. 📅 Schedule it with cron (optional)
3. 🏷️ Add more tags as you solve more problems
4. 🌟 Star your repository!

---

## 🆘 Still Having Issues?

1. Check logs: `logs/sync.log`
2. Verify all configurations
3. Make sure credentials are fresh and valid
4. Test internet connection to leetcode.com and github.com

---

**Happy syncing!** 🎉
