# 🏗️ Auto Repository Creation Feature

## ✨ What This Does

The app now **automatically checks if your GitHub repository exists** and offers to create it if it doesn't!

## 🎯 How It Works

When you run `python3 main.py`, the app will:

1. ✅ **Check if repository exists**
   - If yes → Continue to sync
   - If no → Ask if you want to create it

2. 🤔 **Ask for confirmation**
   ```
   Checking GitHub repository...
   ⚠️  Repository 'leetcode-solutions' not found.
   Would you like to create it now? [Y/n]:
   ```

3. ✅ **Create automatically**
   - Creates the repository with your configured name
   - Sets it as public by default
   - Initializes with a README
   - Shows you the URL

4. 🚀 **Continue to sync**
   - Proceeds with the normal sync process

## 🎨 Configure Repository Name

You can change the repository name in `config/config.yaml`:

```yaml
github:
  username: "your_username"
  repository: "my-leetcode-solutions"  # ← Change this!
```

**Examples of custom names:**
- `"leetcode-solutions"`
- `"my-coding-journey"`
- `"algorithm-practice"`
- `"interview-prep"`
- `"sql-solutions"`

## 🔧 Repository Settings

The auto-created repository will have:
- ✅ **Visibility:** Public (visible to everyone)
- ✅ **README:** Auto-initialized
- ✅ **Default Branch:** main
- ✅ **Description:** "🚀 LeetCode solutions automatically synced from my LeetCode account"

### Want Private Repository?

If you want the repository to be **private**, you can:

**Option 1:** Create it manually first:
1. Go to https://github.com/new
2. Name it (same as in config.yaml)
3. Choose "Private"
4. Create repository

**Option 2:** Modify the code in `src/core/github_client.py`:
```python
# Line in create_repository method:
private=True,  # Change False to True
```

## 📝 Standalone Script (Optional)

If you want to create the repository separately without running the sync:

```bash
python3 create_repo.py
```

This script:
- Creates the repository
- Shows the URL
- Exits (doesn't run sync)

## 🎯 Use Cases

### First Time User
```bash
# Just configured your settings
python3 main.py

# Output:
Checking GitHub repository...
⚠️  Repository 'leetcode-solutions' not found.
Would you like to create it now? [Y/n]: y

Creating repository 'leetcode-solutions'...
✅ Repository created: https://github.com/username/leetcode-solutions

✓ Repository 'leetcode-solutions' found
Testing connections...
```

### Changed Repository Name
```yaml
# Updated config.yaml:
repository: "my-new-leetcode-repo"
```

```bash
python3 main.py

# Will check for 'my-new-leetcode-repo'
# If doesn't exist, offers to create it
```

### Repository Already Exists
```bash
python3 main.py

# Output:
Checking GitHub repository...
✓ Repository 'leetcode-solutions' found

Testing connections...
# Continues normally
```

## 🛡️ Error Handling

### Token Permissions
If creation fails, you might need to check your GitHub token has `repo` scope:

1. Go to https://github.com/settings/tokens
2. Click on your token
3. Ensure ✅ `repo` is checked
4. Regenerate if needed

### Repository Name Taken
If the name is already taken by another user:
- The script will notify you
- Choose a different name in `config.yaml`
- Run again

### Network Issues
If creation fails due to network:
- Check internet connection
- Try again
- Create manually as backup

## 📊 Summary

| Feature | Status |
|---------|--------|
| **Auto-detection** | ✅ Yes |
| **Auto-creation** | ✅ Yes (with confirmation) |
| **Configurable name** | ✅ Yes (config.yaml) |
| **Skip if exists** | ✅ Yes |
| **Public by default** | ✅ Yes |
| **Can be private** | ✅ Yes (manual or code change) |

---

**✨ No more manual repository creation needed!** Just configure and run!
