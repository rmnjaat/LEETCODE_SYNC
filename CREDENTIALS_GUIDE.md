# 🔑 Credentials Guide - How to Get Your API Keys

This guide explains exactly how to obtain the credentials needed for the LeetCode to GitHub Sync tool.

---

## 📋 What You Need

You need **3 credentials**:

1. ✅ `LEETCODE_SESSION` - Cookie from your browser
2. ✅ `LEETCODE_CSRF_TOKEN` - Cookie from your browser  
3. ✅ `GITHUB_TOKEN` - Personal Access Token from GitHub

---

## 🍪 Part 1: Getting LeetCode Cookies

### Step-by-Step Instructions

#### 1️⃣ Login to LeetCode

Go to [https://leetcode.com](https://leetcode.com) and login to your account.

#### 2️⃣ Open Developer Tools

**Windows/Linux:**
- Press `F12`
- OR Right-click anywhere → Select "Inspect"

**Mac:**
- Press `Cmd + Option + I`
- OR Right-click anywhere → Select "Inspect Element"

#### 3️⃣ Navigate to Cookies Section

**Chrome / Edge / Brave:**
```
1. Click "Application" tab at the top of DevTools
2. In left sidebar: Expand "Storage" → "Cookies"
3. Click on "https://leetcode.com"
```

**Firefox:**
```
1. Click "Storage" tab at the top of DevTools
2. In left sidebar: Expand "Cookies"
3. Click on "https://leetcode.com"
```

**Safari:**
```
1. First enable developer tools:
   Safari → Preferences → Advanced → ✅ Show Develop menu
2. Right-click page → Inspect Element
3. Click "Storage" tab
4. Expand "Cookies" → Click "leetcode.com"
```

#### 4️⃣ Find and Copy LEETCODE_SESSION

You'll see a table with columns: **Name | Value | Domain | Path | Expires**

1. Look for the row where **Name** = `LEETCODE_SESSION`
2. Copy the **Value** (it's a long string of random characters)
3. It looks something like: `eyJ0eXAiOiJKV1QiLCJhbGciOiJS...` (much longer)

**Tips:**
- Double-click the Value to select it all
- Use `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac) to copy
- The value is usually 200-500 characters long

#### 5️⃣ Find and Copy LEETCODE_CSRF_TOKEN

In the same cookies table:

1. Look for the row where **Name** = `csrftoken`
2. Copy the **Value**
3. It's shorter than the session cookie

---

## 🔐 Part 2: Getting GitHub Personal Access Token

### Step-by-Step Instructions

#### 1️⃣ Go to GitHub Token Settings

**Direct Link:** [https://github.com/settings/tokens](https://github.com/settings/tokens)

**OR Manual Navigation:**
```
1. Click your profile picture (top-right)
2. Settings
3. Scroll down to "Developer settings" (left sidebar, at the bottom)
4. Personal access tokens
5. Tokens (classic)
```

#### 2️⃣ Generate New Token

Click the button: **"Generate new token" → "Generate new token (classic)"**

> ⚠️ Use "classic" tokens, not the new "fine-grained" tokens

#### 3️⃣ Configure Your Token

**Note (Description):**
```
LeetCode to GitHub Sync
```

**Expiration:**
- Choose: `30 days`, `60 days`, `90 days`, or `No expiration`
- Recommended: `90 days` (you'll need to regenerate it after)

**Select Scopes:**

Scroll down and check these boxes:

```
✅ repo
   ✅ repo:status
   ✅ repo_deployment  
   ✅ public_repo
   ✅ repo:invite
   ✅ security_events
```

> ⚠️ **IMPORTANT:** You MUST check the `repo` scope!  
> This gives the tool permission to create and update files in your repository.

**Do NOT check these (not needed):**
- ❌ workflow
- ❌ write:packages
- ❌ delete:packages
- ❌ admin:org
- ❌ admin:public_key
- ❌ admin:repo_hook
- ❌ admin:org_hook
- ❌ gist
- ❌ notifications
- ❌ user
- ❌ delete_repo
- ❌ write:discussion
- ❌ admin:enterprise

#### 4️⃣ Generate and Copy Token

1. Scroll to the bottom
2. Click **"Generate token"**
3. **IMMEDIATELY COPY THE TOKEN!**
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You will NOT be able to see it again!
   - If you lose it, you'll need to generate a new one

**Save it somewhere safe temporarily** (like a password manager or temporary note)

---

## 💾 Part 3: Save Credentials to .env File

#### 1️⃣ Copy the Template

```bash
cd "/Users/ramanjangu/Desktop/Leetcode project"
cp env.example .env
```

#### 2️⃣ Edit the .env File

Open it in your favorite editor:

```bash
# Using nano:
nano .env

# Using VS Code:
code .env

# Using any text editor:
open .env
```

#### 3️⃣ Paste Your Credentials

Replace the placeholder text with your actual values:

```env
# Before (template):
LEETCODE_SESSION=your_session_cookie_here
LEETCODE_CSRF_TOKEN=your_csrf_token_here
GITHUB_TOKEN=your_github_personal_access_token_here

# After (with your real values):
LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
LEETCODE_CSRF_TOKEN=Bq8ks8TYPmRgQx5JhV3L...
GITHUB_TOKEN=ghp_AbCdEfGhIjKlMnOpQrStUvWxYz123456...
```

#### 4️⃣ Save the File

- **Nano:** `Ctrl+O` → `Enter` → `Ctrl+X`
- **VS Code:** `Cmd/Ctrl+S`
- **Text Editor:** File → Save

---

## ✅ Part 4: Verify Your Setup

Run this command to test:

```bash
conda activate leetcode-project
python main.py
```

If everything is correct, you'll see:
```
Testing connections...
✓ LeetCode connection test successful
✓ GitHub connection test successful
```

---

## 🔧 Troubleshooting

### Problem: "LEETCODE_SESSION not set"

**Causes:**
- File is named `env.example` instead of `.env`
- Empty value in .env file
- Extra spaces or quotes around the value

**Solution:**
```bash
# Make sure file is named .env (with the dot!)
ls -la | grep env

# Should show: .env (not env.example)
```

**Check your .env file:**
- No spaces around the `=` sign
- No quotes around values
- Values should be on the same line

### Problem: "Failed to authenticate with LeetCode"

**Causes:**
- Session cookie expired
- Copied cookie incorrectly
- Not logged into LeetCode

**Solution:**
1. Logout from LeetCode completely
2. Login again
3. Get fresh cookies (follow Part 1 again)
4. Update .env file

### Problem: "Failed to connect to GitHub repository"

**Causes:**
- GitHub token doesn't have `repo` scope
- Token expired
- Token copied incorrectly

**Solution:**
1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Delete the old token
3. Generate a new one with `repo` scope checked
4. Update .env file

### Problem: Cookies table is empty in DevTools

**Solution:**
- Make sure you're logged into LeetCode
- Refresh the page (F5)
- Make sure you're on leetcode.com (not leetcode.cn)

### Problem: Can't find "Application" tab in DevTools

**Chrome/Edge:**
- Click the `>>` icon if there are too many tabs
- Look for "Application" in the dropdown

**Firefox:**
- It's called "Storage" tab instead

### Problem: Token disappeared from GitHub

**Solution:**
- GitHub only shows the token once for security
- If you lost it, generate a new one
- Save it in a password manager for future reference

---

## 📱 Browser-Specific Guides

### Google Chrome / Microsoft Edge / Brave

```
1. F12 or Right-click → Inspect
2. "Application" tab
3. Left sidebar: Storage → Cookies → https://leetcode.com
4. Find LEETCODE_SESSION and csrftoken
5. Copy the Value column
```

### Mozilla Firefox

```
1. F12 or Right-click → Inspect Element
2. "Storage" tab
3. Left sidebar: Cookies → https://leetcode.com
4. Find LEETCODE_SESSION and csrftoken
5. Copy the Value column
```

### Safari

```
1. Safari → Preferences → Advanced
2. ✅ Show Develop menu in menu bar
3. Right-click page → Inspect Element
4. "Storage" tab
5. Cookies → leetcode.com
6. Find LEETCODE_SESSION and csrftoken
7. Copy the Value column
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep your `.env` file secure and private
- Never commit `.env` to Git (already in `.gitignore`)
- Regenerate tokens periodically
- Use expiring tokens (30/60/90 days)
- Store tokens in a password manager

### ❌ DON'T:
- Share your tokens with anyone
- Post them in Discord/Slack/forums
- Commit them to public repositories
- Use the same token across multiple tools
- Leave tokens with "no expiration" (security risk)

---

## 📸 Visual Reference

### What LeetCode Cookies Look Like:

```
┌─────────────────────┬──────────────────────────────────────┐
│ Name                │ Value                                │
├─────────────────────┼──────────────────────────────────────┤
│ LEETCODE_SESSION    │ eyJ0eXAiOiJKV1QiLCJhbGciOiJS...     │ ← Copy this!
│ csrftoken           │ Bq8ks8TYPmRgQx5JhV3L...             │ ← Copy this!
│ _ga                 │ GA1.2.123456789.1234567890          │
│ _gid                │ GA1.2.987654321.0987654321          │
└─────────────────────┴──────────────────────────────────────┘
```

### What GitHub Token Looks Like:

```
Format: ghp_[40 random characters]

Example: ghp_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890

Length: 40 characters (after ghp_ prefix)
```

---

## ⏱️ How Long Do Credentials Last?

| Credential | Duration | Refresh Method |
|------------|----------|----------------|
| `LEETCODE_SESSION` | ~30 days* | Logout & login again |
| `LEETCODE_CSRF_TOKEN` | ~30 days* | Logout & login again |
| `GITHUB_TOKEN` | As configured | Generate new token |

*Exact duration varies; LeetCode may expire sessions earlier if suspicious activity is detected

---

## 🆘 Still Need Help?

1. Check `SETUP_GUIDE.md` for step-by-step setup
2. Check `README.md` for usage instructions
3. Check logs: `logs/sync.log`
4. Make sure you're using the correct browser (try Chrome if issues persist)
5. Verify you're logged into the correct LeetCode account

---

## ✅ Quick Checklist

Before running the sync:

- [ ] Logged into LeetCode in browser
- [ ] Copied `LEETCODE_SESSION` from cookies
- [ ] Copied `csrftoken` from cookies
- [ ] Generated GitHub token with `repo` scope
- [ ] Created `.env` file (not `env.example`)
- [ ] Pasted all three credentials into `.env`
- [ ] No extra spaces, quotes, or special characters
- [ ] Saved the `.env` file

**Ready to sync?** Run: `python main.py`

---

**🎉 You're all set! Your credentials are configured and ready to use!**
