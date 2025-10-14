# CLAUDE.MD - VAL INFANTE'S VISUALIZATION REPOSITORY

**Owner:** Val Infante (NOT Val Diaz)
**GitHub:** vinfante1346
**Repository:** https://github.com/vinfante1346/visualizations
**Live URL:** https://vinfante1346.github.io/visualizations/

---

## 🔒 Dashboard Password

**Default Password:** `valinfante2025`

The root dashboard (index.html) is password-protected. Users must enter the password to access the full catalog of visualizations.

**To change the password:**
1. Edit `/visualizations/index.html`
2. Find the `validPasswordHash` variable
3. Generate new hash for your password using SHA-256
4. Update the plain password check on line with `password === 'valinfante2025'`

---

## Repository Purpose

This is **Val Infante's** central repository for deploying interactive web visualizations, dashboards, business models, and presentations to GitHub Pages.

All files are publicly accessible at: `https://vinfante1346.github.io/visualizations/`

---

## Critical Rules

### ⚠️ NEVER BREAK THESE

1. **Always use `vinfante1346`, NEVER `pwatson`**
   - ❌ WRONG: `https://pwatson-mybambu.github.io/...`
   - ✅ CORRECT: `https://vinfante1346.github.io/...`

2. **Owner is Val Infante, NOT Val Diaz**

3. **All visualization files go in `/artifacts/` directory**
   - Root-level files: Dashboard utilities, forecasts, comparisons
   - artifacts/: Individual presentations and visualizations

4. **Always push from this directory:**
   ```
   /Users/vinfa/Desktop/Development Claude/visualizations
   ```

---

## Repository Structure

```
visualizations/
├── index.html              # 🔒 Password-protected dashboard (ROOT)
├── artifacts/              # Individual visualizations (publicly accessible)
│   ├── apoyo-mybambu-leverage-calculator.html
│   ├── mybambu-overview.html
│   ├── customer-stickiness.html
│   ├── bambu-pay-*.html
│   └── [other visualizations]
├── forecast-dashboard.html # Root-level utilities
├── circle-vs-kira-comparison.html
├── mybambu-crypto-wallet-forecast.html
├── vendor-analysis.html
├── mybambu-deposit-options.html
├── README.md
├── CLAUDE.md              # This file
└── deploy.sh
```

---

## Deployment Workflow

### Standard Deployment

```bash
# 1. Navigate to repository
cd /Users/vinfa/Desktop/Development\ Claude/visualizations

# 2. Add files
git add .

# 3. Commit
git commit -m "Add [description]"

# 4. Push
git push
```

### Quick Deploy Script

```bash
cd /Users/vinfa/Desktop/Development\ Claude/visualizations
./deploy.sh artifacts/filename.html "Description"
```

---

## URL Patterns

**Root Dashboard (Password Protected):**
```
https://vinfante1346.github.io/visualizations/
```

**Individual Visualizations:**
```
https://vinfante1346.github.io/visualizations/artifacts/[filename].html
```

**Root-Level Tools:**
```
https://vinfante1346.github.io/visualizations/[filename].html
```

---

## File Naming Standards

✅ **Good filenames:**
- `apoyo-mybambu-leverage-calculator.html`
- `customer-stickiness-analysis.html`
- `q4-sales-dashboard.html`

❌ **Bad filenames:**
- `file1.html` (not descriptive)
- `my report.html` (has spaces)
- `Sales_Dashboard.html` (uses underscores)

**Rules:**
- Use hyphens (`-`), not spaces or underscores
- All lowercase
- Descriptive and clear
- End with `.html`

---

## Creating New Visualizations

When Claude Code creates a new visualization:

1. **Create self-contained HTML file**
   - All CSS inline in `<style>` tags
   - All JavaScript inline in `<script>` tags
   - No external dependencies (except CDN libraries if necessary)

2. **Save to `/artifacts/` directory**
   ```bash
   /Users/vinfa/Desktop/Development Claude/visualizations/artifacts/new-viz.html
   ```

3. **Use descriptive, hyphenated filename**

4. **Deploy immediately**
   ```bash
   cd /Users/vinfa/Desktop/Development\ Claude/visualizations
   git add artifacts/new-viz.html
   git commit -m "Add new visualization"
   git push
   ```

5. **Provide URL to user**
   ```
   https://vinfante1346.github.io/visualizations/artifacts/new-viz.html
   ```

6. **Wait 1-2 minutes for GitHub Pages deployment**

---

## Design Guidelines

All visualizations should be:
- **Self-contained**: No external CSS/JS files
- **Responsive**: Mobile-friendly design
- **Professional**: Clean, modern styling
- **Interactive**: Use JavaScript for interactivity where appropriate
- **Fast**: Optimize for quick loading

**Preferred Style:**
- Clean gradients
- Card-based layouts
- Smooth transitions
- Modern color schemes (blues, purples, greens)
- System fonts

---

## Dashboard Management

The root `index.html` is a password-protected dashboard that catalogs ALL visualizations.

**When adding new visualizations:**
1. Add new card to appropriate section in `index.html`
2. Include proper metadata (title, description, keywords)
3. Link to correct URL
4. Update total count

**Sections:**
- Business Models & Analytics
- Company Overviews
- Product Presentations
- Documentation & Testing

---

## Pre-Deployment Checklist

Before sharing URLs with Val Infante:

- [ ] File is in correct directory (`artifacts/` or root)
- [ ] Filename follows naming standards
- [ ] Pushed from `/Users/vinfa/Desktop/Development Claude/visualizations`
- [ ] URL uses `vinfante1346` (not pwatson)
- [ ] Waited 1-2 minutes after push
- [ ] Tested URL (optional but recommended)

---

## Common Mistakes to Avoid

❌ **DO NOT:**
1. Use `pwatson` in URLs
2. Call owner "Val Diaz" (it's Val Infante)
3. Push from wrong directory
4. Use spaces in filenames
5. Create external CSS/JS files
6. Forget to update dashboard when adding files

✅ **DO:**
1. Always use `vinfante1346`
2. Remember owner is Val Infante
3. Push from correct directory
4. Use hyphenated filenames
5. Keep everything self-contained
6. Update dashboard index

---

## GitHub Pages Settings

**Current Configuration:**
- Source: `main` branch
- Folder: `/ (root)`
- Deployment: Automatic on push
- Live URL: `https://vinfante1346.github.io/visualizations/`

**Do NOT change these without approval.**

---

## Quick Reference

**Repository Path:**
```
/Users/vinfa/Desktop/Development Claude/visualizations
```

**Git Remote:**
```
git@github.com:vinfante1346/visualizations.git
```

**Public URL Base:**
```
https://vinfante1346.github.io/visualizations/
```

**Dashboard Password:**
```
valinfante2025
```

---

**Last Updated:** January 14, 2025
**Owner:** Val Infante
**Maintained By:** Claude Code
