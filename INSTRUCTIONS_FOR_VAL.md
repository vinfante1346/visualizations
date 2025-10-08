# 🚀 How to Deploy Your Visualizations

## Your Live Site
**https://pwatson-mybambu.github.io/visualizations/**

---

## 🤖 EASIEST WAY: Automated with Claude Desktop (Recommended!)

### One-Time Setup (5 minutes):
See **[CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)** for detailed instructions.

**Quick version:**
1. Open `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Copy the contents from `CLAUDE_INSTRUCTIONS.txt`
3. Restart Claude Desktop

### After Setup:
Just say to Claude:
```
"Create a sales dashboard and give me a public link"
```

Claude will automatically:
- ✅ Create the HTML file
- ✅ Save it to the artifacts folder
- ✅ Deploy it to GitHub Pages
- ✅ Give you the public URL

**That's it!** No manual deployment needed.

---

## 📝 Manual Method (If you prefer doing it yourself)

### Step 1: Create in Claude Desktop
Ask Claude to create whatever you need (dashboard, report, visualization, etc.)

### Step 2: Save the HTML File
1. Tell Claude: "Show me the complete HTML code"
2. Copy all the code
3. Save it in the `artifacts` folder with a descriptive name
   - Example: `artifacts/q4-sales-report.html`
   - Use hyphens, not spaces in filenames

### Step 3: Deploy It
Open Terminal and run:

```bash
cd ~/Documents/visualizations
./deploy.sh q4-sales-report.html "Q4 sales report"
```

**That's it!** Wait 1-2 minutes, then share your link.

---

## 🔗 Your Link Format
```
https://pwatson-mybambu.github.io/visualizations/artifacts/[your-filename].html
```

Example:
```
https://pwatson-mybambu.github.io/visualizations/artifacts/q4-sales-report.html
```

---

## 🆘 First Time Setup (One-Time Only)

If you haven't cloned the repo yet:

```bash
cd ~/Documents
git clone https://github.com/pwatson-mybambu/visualizations.git
cd visualizations
chmod +x deploy.sh
```

Configure git with your info:
```bash
git config user.name "Val Diaz"
git config user.email "val@mybambu.com"
```

---

## 💡 Tips

✅ **Name files clearly**: `client-presentation-2024.html` not `file1.html`
✅ **Use hyphens**: `my-report.html` not `my report.html`
✅ **Wait 1-2 minutes** after deploying for changes to appear
✅ **Anyone with the link can view** - share carefully

---

## 🔧 Alternative: Manual Deploy (Without Script)

If the deploy script doesn't work:

```bash
cd ~/Documents/visualizations
git add .
git commit -m "Add your description here"
git push
```

---

## ❓ Common Issues

**"Permission denied" when running deploy.sh?**
```bash
chmod +x deploy.sh
```

**Want to see what files you have?**
```bash
ls artifacts/
```

**Want to pull latest changes?**
```bash
git pull
```

---

Need help? Ask Patrick! 📞
