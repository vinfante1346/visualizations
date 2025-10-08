# AI Agent Configuration for Visualizations Repository

This file provides instructions for AI agents (Claude Code, GitHub Copilot, etc.) working in this repository.

---

## Repository Purpose

This repository is for **Val Diaz** to deploy interactive web visualizations, dashboards, and reports to GitHub Pages.

**Live Site**: https://pwatson-mybambu.github.io/visualizations/

---

## Core Principles

1. **Simplicity First**: Val is not a developer. Everything should be as simple as possible.
2. **Automation Preferred**: Claude Desktop automation is the recommended workflow.
3. **Clean File Naming**: Always use hyphenated, descriptive filenames (e.g., `q4-sales-report.html`)
4. **GitHub Pages**: All artifacts are deployed to GitHub Pages automatically.

---

## Repository Structure

```
visualizations/
├── artifacts/               # ← Val's HTML files go here (publicly accessible)
│   ├── test.html           # Test page with purple gradient
│   └── instructions.html   # Interactive guide with tabs
├── archives/               # For old/archived visualizations
├── templates/              # Reusable HTML templates
├── deploy.sh              # One-command deploy script
├── CLAUDE.md              # This file - AI agent instructions
├── CLAUDE_INSTRUCTIONS.txt # Instructions for Claude Desktop config
├── CLAUDE_DESKTOP_SETUP.md # How to configure Claude Desktop
├── INSTRUCTIONS_FOR_VAL.md # User-facing instructions
├── SETUP_SUMMARY.md       # Complete setup reference
└── README.md              # Repository overview
```

---

## File Naming Standards

**ALWAYS follow these rules when creating files:**

✅ **Good filenames:**
- `q4-sales-dashboard.html`
- `client-presentation-2024.html`
- `revenue-analysis.html`

❌ **Bad filenames:**
- `file1.html` (not descriptive)
- `my report.html` (has spaces)
- `Sales_Dashboard.html` (uses underscores instead of hyphens)

**Rules:**
1. Use hyphens (`-`), not spaces or underscores
2. All lowercase
3. Descriptive and clear
4. End with `.html`
5. No special characters except hyphens

---

## When Creating HTML Visualizations

### Standard Template Pattern

All HTML files should be **self-contained** with:
- Complete HTML structure (`<!DOCTYPE html>`, `<head>`, `<body>`)
- Inline CSS styles (no external stylesheets)
- Inline JavaScript if needed (no external scripts)
- Responsive design (mobile-friendly)
- Modern, professional styling

### Design Guidelines

**Preferred style approach:**
- Clean, modern design with gradients
- Card-based layouts
- Subtle animations (fade-in, hover effects)
- Professional color schemes (blues, purples, greens)
- Good typography (system fonts like `-apple-system, BlinkMacSystemFont`)
- Responsive grid layouts

**Example starter template:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Title Here</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        /* Add more styles as needed */
    </style>
</head>
<body>
    <div class="container">
        <!-- Content here -->
    </div>
</body>
</html>
```

---

## Multi-Page Visualizations

When creating multiple linked pages:

1. **Save all pages** to the `artifacts/` folder
2. **Use relative links** between pages:
   ```html
   <!-- ✅ Correct -->
   <a href="details.html">View Details</a>

   <!-- ❌ Wrong - don't use full URLs -->
   <a href="https://pwatson-mybambu.github.io/visualizations/artifacts/details.html">View Details</a>
   ```
3. **Include navigation** on each page
4. **Deploy all pages together** in a single commit

---

## Deployment Process

### Automated Method (Recommended)

When Val has Claude Desktop configured, he'll simply say:
```
"Create a sales dashboard and give me a public link"
```

Claude Desktop will automatically:
1. Create the HTML file
2. Save it to `~/Documents/visualizations/artifacts/`
3. Run git commands to deploy
4. Provide the public URL

### Manual Deployment

If Val needs to deploy manually:

```bash
cd ~/Documents/visualizations
./deploy.sh filename.html "Description of changes"
```

Or with raw git commands:
```bash
git add .
git commit -m "Add filename"
git push
```

---

## Working with This Repository

### As Claude Code (in this workspace):

When asked to help with this repository:

1. **Always save files** to the `artifacts/` folder
2. **Use descriptive filenames** with hyphens
3. **Create self-contained HTML** (all CSS/JS inline)
4. **Test responsiveness** (works on mobile and desktop)
5. **Commit and push** after creating/updating files

### As Claude Desktop (Val's setup):

When Val asks to create visualizations:

1. **Create the HTML** with complete, professional styling
2. **Save to** `~/Documents/visualizations/artifacts/[descriptive-name].html`
3. **Deploy** by running:
   ```bash
   cd ~/Documents/visualizations
   git add .
   git commit -m "Add [description]"
   git push
   ```
4. **Provide URL** to Val:
   ```
   https://pwatson-mybambu.github.io/visualizations/artifacts/[filename].html
   ```
5. **Remind** to wait 1-2 minutes for GitHub Pages to update

---

## Common Tasks

### Creating a New Visualization

1. Ask Val what kind of visualization he needs
2. Create a self-contained HTML file
3. Save to `artifacts/` with descriptive name
4. Deploy using `./deploy.sh` or git commands
5. Provide the public URL

### Updating an Existing Visualization

1. Locate the file in `artifacts/`
2. Make requested changes
3. Save the updated file (overwrite existing)
4. Deploy with commit message like "Update [filename] - [what changed]"
5. Remind that URL stays the same (will update after 1-2 minutes)

### Creating Multi-Page Sites

1. Create all HTML pages with relative links
2. Save all to `artifacts/` folder
3. Deploy all together in single commit
4. Provide all public URLs in a list

---

## GitHub Pages URLs

**Format:**
```
https://pwatson-mybambu.github.io/visualizations/artifacts/[filename].html
```

**Examples:**
- `https://pwatson-mybambu.github.io/visualizations/artifacts/q4-sales-dashboard.html`
- `https://pwatson-mybambu.github.io/visualizations/artifacts/client-presentation.html`

**Deployment Time:** 1-2 minutes after pushing to GitHub

---

## Best Practices

### File Organization
- ✅ Keep active visualizations in `artifacts/`
- ✅ Move old/unused files to `archives/`
- ✅ Save reusable templates to `templates/`
- ✅ Use clear, descriptive filenames

### Code Quality
- ✅ Self-contained HTML (no external dependencies)
- ✅ Responsive design (mobile-first)
- ✅ Clean, commented code
- ✅ Professional styling
- ✅ Fast loading (no heavy libraries unless necessary)

### Git Commits
- ✅ Descriptive commit messages: "Add Q4 sales dashboard"
- ✅ Commit related changes together
- ✅ Push frequently (changes go live quickly)

### User Experience
- ✅ Simple, intuitive interfaces
- ✅ Clear navigation (for multi-page sites)
- ✅ Professional appearance
- ✅ Fast loading times
- ✅ Works on all devices

---

## Don'ts

❌ **Don't** use spaces in filenames
❌ **Don't** create files outside the `artifacts/` folder (unless templates/archives)
❌ **Don't** use external CSS/JS files (keep everything inline)
❌ **Don't** use absolute URLs for navigation between pages
❌ **Don't** forget to commit and push after creating files
❌ **Don't** create overly complex visualizations (keep it simple for Val)
❌ **Don't** use technologies that require build steps (no React, Vue, etc. - just HTML/CSS/JS)

---

## Reference Files

- **For Val**: [INSTRUCTIONS_FOR_VAL.md](INSTRUCTIONS_FOR_VAL.md)
- **For Claude Desktop Setup**: [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)
- **Setup Summary**: [SETUP_SUMMARY.md](SETUP_SUMMARY.md)
- **Deploy Script**: [deploy.sh](deploy.sh)

---

## Support

If you're unsure about something:
1. Check the [SETUP_SUMMARY.md](SETUP_SUMMARY.md) for context
2. Look at existing files in `artifacts/` for examples
3. Follow the patterns in [instructions.html](artifacts/instructions.html)
4. When in doubt, keep it simple!

---

**Last Updated:** 2025-10-08
**Repository Owner:** Val Diaz
**Maintainer:** Patrick Watson
