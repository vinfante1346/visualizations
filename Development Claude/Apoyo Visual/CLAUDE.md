# CLAUDE.MD - VAL'S GITHUB CONFIGURATION

**CRITICAL: READ THIS EVERY TIME BEFORE DEPLOYING ANYTHING**

---

## Val's GitHub Account

**GitHub Username:** `vinfante1346`

**GitHub Pages Base URL:** `https://vinfante1346.github.io`

---

## Repository Structure

Val has ONE main repository for all visualizations and projects:

**Repository Name:** `visualizations`
**Git Remote:** `git@github.com:vinfante1346/visualizations.git`
**GitHub Pages URL:** `https://vinfante1346.github.io/visualizations/`

---

## Project Organization

All projects live in subdirectories of the `visualizations` repository:

```
visualizations/
├── artifacts/               # General visualizations
├── forecast-dashboard/      # Forecast dashboard project
├── apoyo-visual/           # Apoyo + BlockWyre project
├── [other-projects]/       # Future projects
└── CLAUDE.md              # This file
```

---

## GitHub Pages Deployment Rules

### ⚠️ ABSOLUTE RULES - NEVER BREAK THESE

1. **Always use vinfante1346, NEVER pwatson**
   - ❌ WRONG: `https://pwatson-mybambu.github.io/...`
   - ✅ CORRECT: `https://vinfante1346.github.io/...`

2. **Repository is always `/visualizations/`**
   - ❌ WRONG: `https://vinfante1346.github.io/apoyo-visual/...`
   - ✅ CORRECT: `https://vinfante1346.github.io/visualizations/...`

3. **File path follows directory structure**
   - File location: `/artifacts/my-file.html`
   - Public URL: `https://vinfante1346.github.io/visualizations/artifacts/my-file.html`

4. **Test URLs before giving to Val**
   - After deploying, wait 2 minutes
   - Verify the URL works before sharing

---

## URL Formula

```
Local Path: /Users/vinfa/Desktop/Development Claude/Apoyo Visual/[folder]/[filename].html
Public URL: https://vinfante1346.github.io/visualizations/[folder]/[filename].html
```

### Examples:

| Local Path | Public URL |
|------------|-----------|
| `artifacts/apoyo-mybambu-leverage-calculator.html` | `https://vinfante1346.github.io/visualizations/artifacts/apoyo-mybambu-leverage-calculator.html` |
| `forecast-dashboard/index.html` | `https://vinfante1346.github.io/visualizations/forecast-dashboard/index.html` |
| `test.html` | `https://vinfante1346.github.io/visualizations/test.html` |

---

## Git Workflow

### Standard Deployment

```bash
cd "/Users/vinfa/Desktop/Development Claude/Apoyo Visual"
git add .
git commit -m "Add [description]"
git push
```

### If Push Fails

```bash
git pull --rebase origin main
git push
```

### If Upstream Not Set

```bash
git push -u origin main
```

---

## GitHub Pages Settings

**Current Configuration:**
- Source: `main` branch
- Folder: `/ (root)`
- Custom domain: None
- Deployment: Automatic on push

**Do NOT change these settings without Val's approval.**

---

## Common Mistakes to Avoid

### ❌ DO NOT:
1. Use `pwatson-mybambu` username (that's someone else's account!)
2. Create new repositories for each project
3. Push to wrong remotes
4. Give Val URLs that 404
5. Forget to wait 1-2 minutes after deployment

### ✅ DO:
1. Always use `vinfante1346` username
2. Keep all projects in the `visualizations` repository
3. Verify git remote before pushing
4. Test URLs before sharing with Val
5. Create subdirectories for different projects

---

## Quick Checklist Before Sharing URLs

- [ ] Username is `vinfante1346` (not pwatson)
- [ ] Repository is `/visualizations/`
- [ ] File path matches directory structure
- [ ] Waited 2 minutes after git push
- [ ] Tested URL in browser (optional but recommended)

---

## Project-Specific Guidelines

### Apoyo + BlockWyre Project
- **Directory:** `artifacts/` or root
- **File naming:** `apoyo-[description].html`
- **URL pattern:** `https://vinfante1346.github.io/visualizations/artifacts/apoyo-[description].html`

### Forecast Dashboard
- **Directory:** `forecast-dashboard/`
- **Main file:** `index.html`
- **URL:** `https://vinfante1346.github.io/visualizations/forecast-dashboard/`

### General Visualizations
- **Directory:** `artifacts/`
- **File naming:** `[descriptive-name].html` (use hyphens, lowercase)
- **URL pattern:** `https://vinfante1346.github.io/visualizations/artifacts/[filename].html`

---

## Emergency Recovery

If you fuck up and push to the wrong repo or give wrong URLs:

1. **Admit the mistake immediately**
2. **Check git remote:** `git remote -v`
3. **Verify repository:** Should be `vinfante1346/visualizations`
4. **Rebuild correct URL** using the formula above
5. **Test before sharing**

---

## Val's Expectations

Val needs:
1. **Correct URLs every time** - No more 404s
2. **Fast deployment** - Push and share link within 2 minutes
3. **Organized structure** - Don't clutter the repo
4. **Professional work** - Test before sharing

---

**REMEMBER: vinfante1346.github.io/visualizations/ - COMMIT THIS TO MEMORY**

---

**Last Updated:** 2025-01-14
**Maintained By:** Claude (that's you, dummy)
