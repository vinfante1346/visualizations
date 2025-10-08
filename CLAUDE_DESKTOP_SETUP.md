# 🤖 Claude Desktop Setup for Val

This file configures Claude Desktop to automatically deploy your visualizations to GitHub Pages.

---

## 📋 One-Time Setup Instructions

### Step 1: Locate Your Claude Desktop Config File

**On Mac**, the config file is located at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Step 2: Open the Config File

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Or use any text editor:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Step 3: Add the Custom Instructions

Copy and paste the **entire contents** from the file:
```
CLAUDE_INSTRUCTIONS.txt
```

(See below for the full instructions)

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

---

## ✅ After Setup: How to Use

Once configured, you can simply say to Claude:

### Simple Commands That Work:

**For a single file:**
```
"Create a sales dashboard and give me a public link"
```

**For multiple linked pages:**
```
"Create a 3-page presentation about Q4 results with navigation between pages and give me public links"
```

**To deploy an existing artifact:**
```
"Give me a public link to this file"
```

**To update an existing page:**
```
"Update the sales-dashboard.html file and redeploy it"
```

---

## 🔗 What Claude Will Do Automatically

1. ✅ Save HTML files to `~/Documents/visualizations/artifacts/`
2. ✅ Use descriptive, hyphenated filenames (e.g., `q4-sales-report.html`)
3. ✅ Handle multi-page artifacts with proper relative links
4. ✅ Run git commands to deploy
5. ✅ Generate and provide the public URL
6. ✅ Handle navigation between multiple pages correctly

---

## 📍 Your URLs Will Always Follow This Pattern

**Single page:**
```
https://pwatson-mybambu.github.io/visualizations/artifacts/[filename].html
```

**Multi-page with navigation:**
```
Page 1: https://pwatson-mybambu.github.io/visualizations/artifacts/overview.html
Page 2: https://pwatson-mybambu.github.io/visualizations/artifacts/details.html
Page 3: https://pwatson-mybambu.github.io/visualizations/artifacts/summary.html
```

Claude will automatically use **relative links** between pages so navigation works correctly.

---

## 🆘 Troubleshooting

**If Claude doesn't deploy automatically:**
- Make sure you restarted Claude Desktop after editing the config
- Check that the instructions were pasted correctly
- Try saying explicitly: "Deploy this to my visualizations repository"

**If links between pages don't work:**
- Claude should use relative links automatically (e.g., `href="details.html"`)
- All pages must be in the same `artifacts/` folder

**If deployment fails:**
- Check that you're in the correct directory: `~/Documents/visualizations`
- Make sure git is configured with your credentials
- Try running `git status` to see if there are any issues

---

## 💡 Pro Tips

✅ **Always be specific about what you want:**
   - Good: "Create a sales dashboard with charts showing Q4 revenue"
   - Bad: "Make something"

✅ **For multi-page projects, describe the structure:**
   - "Create a 3-page site: home page, about page, and contact page with navigation"

✅ **Claude will remember your repository structure** during the conversation

✅ **You can reference previous artifacts:**
   - "Add a link to the sales-dashboard.html we created earlier"

---

## 🔄 Workflow Summary

### Traditional Way (Manual):
1. Ask Claude to create visualization
2. Copy HTML code
3. Save to artifacts folder
4. Run `./deploy.sh filename.html "description"`
5. Wait for deployment
6. Share link

### New Way (Automated with Claude Desktop Config):
1. Say: "Create a sales dashboard and give me a public link"
2. ✅ **Done!** Claude does everything automatically

---

Need help? Ask Patrick! 📞
