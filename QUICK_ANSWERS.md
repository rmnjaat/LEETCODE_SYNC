# Quick Answers to Your Questions

## ❓ "How will you get data from LeetCode? Clear that."

### Answer: Using LeetCode's Official GraphQL API

**API Endpoint:** `https://leetcode.com/graphql`

**Step-by-step process:**

1. **Authentication:**
   - You login to LeetCode in your browser
   - Extract your `LEETCODE_SESSION` cookie from browser developer tools
   - Our Python script uses this cookie to authenticate API requests

2. **Fetching Submissions:**
   ```
   Request → LeetCode API → Response with submission list
   For each submission:
     Request submission details → Get full code + problem info
   ```

3. **What We Get:**
   - ✅ Your actual submitted code
   - ✅ Submission timestamp
   - ✅ Problem title, description, difficulty
   - ✅ Problem tags (like "Database", "Array", etc.)
   - ✅ Status (Accepted/Wrong Answer)
   - ✅ Runtime and memory stats

**No web scraping, no hacks - we use LeetCode's legitimate API!**

---

## ❓ "Currently there will be only one tag as databases"

### Answer: Focused on Database Tag Only

**Implementation:**
- Script will fetch ALL your submissions
- Filter to keep ONLY problems tagged with "Database"
- Ignore problems with other tags (Array, Tree, etc.)
- Save everything in a folder: `Databases/`

**Easy to extend later:**
- Want to add more tags? Just update config file
- Can support multiple tags: ["Database", "Array", "Dynamic Programming"]
- Each tag gets its own folder

---

## ❓ "It should give choice like for how many last days submission to look for"

### Answer: User Selects Date Range at Runtime

**How it works:**

```bash
$ python main.py

How many days back should I fetch submissions?
  [1] Last 7 days
  [2] Last 30 days
  [3] Last 60 days
  [4] Last 90 days
  [5] All time

Enter your choice: 2

✓ Fetching submissions from last 30 days...
```

**OR** can be set in config file:
```yaml
sync_settings:
  days_to_look_back: 30  # Change this anytime
```

**What happens:**
- Script calculates cutoff date: Today - N days
- Converts to timestamp
- Only fetches submissions newer than that date
- Ignores older submissions

**Example:**
- Today: Oct 4, 2024
- You choose: 30 days
- Cutoff: Sep 4, 2024
- Result: Only submissions between Sep 4 - Oct 4 are fetched

---

## ❓ "What will you do if multiple solutions for one question exists?"

### Answer: Keep ALL Solutions with Version Numbers

**Scenario:**
You solved "Combine Two Tables" three times:
- Sep 20, 2024 (first attempt)
- Sep 25, 2024 (improved)
- Oct 2, 2024 (optimized)

**What we do: Save ALL THREE**

### File Naming Strategy:

**Option 1: Version Numbers (Recommended)**
```
Databases/
├── combine-two-tables_v1.sql    ← Sep 20 solution
├── combine-two-tables_v2.sql    ← Sep 25 solution
└── combine-two-tables_v3.sql    ← Oct 2 solution
```

**Option 2: Timestamps**
```
Databases/
├── combine-two-tables_20240920_143022.sql
├── combine-two-tables_20240925_091534.sql
└── combine-two-tables_20241002_161245.sql
```

### File Content Example:

**combine-two-tables_v1.sql:**
```sql
/*
 * Problem: 175. Combine Two Tables
 * Link: https://leetcode.com/problems/combine-two-tables/
 * Difficulty: Easy
 * Tags: Database
 * 
 * Submission Info:
 * - Version: 1 of 3
 * - Submitted: 2024-09-20 14:30:22
 * - Status: Accepted
 * - Runtime: 567ms
 * - Memory: 0KB
 * 
 * Problem Description:
 * Table: Person
 * +-------------+---------+
 * | Column Name | Type    |
 * +-------------+---------+
 * | personId    | int     |
 * | firstName   | varchar |
 * | lastName    | varchar |
 * +-------------+---------+
 * ...
 */

-- My Solution (First Attempt):
SELECT 
    p.firstName, 
    p.lastName, 
    a.city, 
    a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

**combine-two-tables_v2.sql:**
```sql
/*
 * (Same metadata but Version: 2 of 3)
 * - Submitted: 2024-09-25 09:15:34
 * - Runtime: 450ms ← Improved!
 */

-- My Solution (Improved):
-- (Different code here - maybe better optimization)
```

### User Control:

You can choose at runtime:
```bash
Multiple solutions detected for these problems:
  - Combine Two Tables: 3 solutions
  - Nth Highest Salary: 2 solutions

How do you want to handle multiple solutions?
  [1] Keep all versions (recommended)
  [2] Keep only the latest
  [3] Keep only the fastest (best runtime)

Enter choice: 1

✓ Keeping all versions with version numbers
```

---

## ❓ "What if I want to keep all of them?"

### Answer: YES! That's the DEFAULT behavior!

**We KEEP ALL SOLUTIONS by default because:**
1. You can see your progress over time
2. Different approaches to same problem
3. Learning opportunity - compare your solutions
4. No data loss - everything is preserved

**You have full control:**
- Config setting: `keep_all_versions: true`
- Or choose at runtime when prompted

**Benefits:**
- Track your improvement
- See different SQL approaches
- Learn from past attempts
- Nothing gets overwritten

---

## 🎯 Summary

| Question | Answer |
|----------|--------|
| **How to get data?** | LeetCode GraphQL API with session cookie authentication |
| **Which tag?** | Only "Database" tag (easy to add more later) |
| **Date range?** | User chooses: 7/30/60/90 days or all-time |
| **Multiple solutions?** | KEEP ALL with version numbers (_v1, _v2, _v3) |
| **Code visibility?** | Full submitted code included in each file |

---

## 🚀 Ready to Build?

**Next Steps:**
1. ✅ You've reviewed the plan
2. ⏭️ I'll create the Python project structure
3. ⏭️ Implement LeetCode API client
4. ⏭️ Implement GitHub uploader
5. ⏭️ Test with your account
6. ⏭️ Sync your Database solutions!

**Sound good? Should I proceed with implementation?** 🎉
