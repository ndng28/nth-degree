# Front-End Best Practices & OpenClaw Integration — nth degree blog

## Current Front-End Best Practices (2026)

### Typography & Readability
- **Fluid type scales** via `clamp()` (already implemented) — the Utopia approach scales perfectly between min/max viewport without breakpoint jumps
- **Measure (line length)**: 65-75 characters per line optimal for reading. Our 740px column with ~17px body text hits ~70-75 chars — ideal
- **Line height**: 1.6-1.8 for body, 1.2-1.3 for headings (met)
- **Font stack**: Variable fonts (Inter) with `opsz` axis for optical sizing at different sizes (already using Inter opsz)
- **System fonts for UI**: Use system UI for nav/meta elements to reduce layout shift

### Color & Contrast
- **Semantic tokens** (already implemented): Named by use, not value (`--text-body`, `--bg-elevated`)
- **WCAG AAA for body text**: ≥7:1 contrast ratio (our dark mode hits ~15.6:1)
- **Dark mode design**: Lower contrast overall (L* 5-12 for backgrounds), lifted accents. Blue accents (#60a5fa) work well for dark mode
- **Light mode design**: Warm neutrals, not pure gray — (#fafafa bg, #f0f0f2 surface) to avoid clinical feel
- **Surface hierarchy**: 3 levels (bg → elevated → raised) creates depth without shadows

### Layout & Spacing
- **Container queries** (CQ): Better than media queries for card components — cards resize based on their container width, not the viewport
- **`max-width` + `margin: 0 auto`**: Standard centered layout. Use a wrapper div (`.page-wrap`), not the body itself, to avoid flexbox `margin: auto` conflicts
- **Space scale**: Use a consistent spacing scale (already using `--space-xs` through `--space-2xl`)
- **Mobile-first**: Start with single column, add complexity at wider breakpoints. 640px/768px/1024px are common breakpoints

### Modern CSS Features (2026)
- **`@supports`** for progressive enhancement (already using for reading progress bar)
- **`scroll-timeline`** (CSS scroll-driven animations): Reading progress bars, parallax effects without JS. ~85% browser support in 2026
- **`prefers-reduced-motion`**: Essential accessibility (already implemented)
- **`prefers-color-scheme`**: Dark/light mode (already using)
- **`color-mix()`**: Create tints/shades dynamically: `color-mix(in srgb, var(--accent) 20%, var(--bg))`
- **`text-wrap: pretty`**: Prevents orphan words on the last line
- **`overscroll-behavior`**: Control scroll chaining

### Performance
- **Zero JS in browser** (already achieved) — massive advantage for Core Web Vitals
- **Inline critical CSS** (already doing via Astro's built-in inlining)
- **Font display: swap** (already using via Google Fonts)
- **Preconnect to font origins** (already using)
- **Image lazy loading**: `loading="lazy"` on content images, explicit `width`/`height` to prevent CLS

### Blog-Specific UX
- **Reading progress bar** (already added via CSS)
- **Next/previous post** navigation — keeps readers on site
- **Related posts by tags** — content discovery
- **Search** (PageFind or MiniSearch for static sites) — essential at 15+ posts
- **OG/social cards** — critical for shareability (basic meta tags added, needs per-post images)
- **RSS feed** (already done) — essential for engineering blog readership

---

## How OpenClaw Can Help

### Direct Capabilities

| OpenClaw Feature | How It Helps the Blog |
|---|---|
| **Sub-agents** | Spawn expert agents (UI/UX, typography, accessibility) for research, audits, and code generation |
| **Canvas skill** | Preview blog design on connected mobile nodes (iOS/Android) — see how it renders on real devices |
| **Cron jobs** | Scheduled tasks: daily build checks, broken link checks, content publishing reminders |
| **Memory (MEMORY.md)** | Store design decisions, color palettes, typography choices, and rationale long-term |
| **Web fetch** | Research best practices, study competitor blogs, fetch inspiration |
| **Exec/shell** | Run build, deploy, CI checks, screenshot capture all from within the session |
| **Sessions** | Persistent chat about design iterations. Track what changed and why |
| **Config/secrets** | Store Cloudflare API keys, GitHub tokens, deployment credentials in 1Password vault |

### Practical Workflows

**1. Design iteration loop**
```
Naveesh: "Fix the padding"
  → I make CSS change
  → I run `npm run build`
  → I start dev server
  → I capture screenshot (Playwright)
  → I send to Telegram
  → Naveesh reviews, gives feedback
  → Repeat
```

**2. Expert audit on demand**
```
Naveesh: "Audit our accessibility"
  → Spawn sub-agent as accessibility expert
  → Sub-agent reads all source files
  → Sub-agent researches WCAG best practices
  → Sub-agent writes report to file
  → I summarize findings
```

**3. Automated maintenance**
```
Cron job (weekly):
  → Clone latest blog repo
  → Run link checker on built output
  → Report broken links
  → Also check for outdated npm packages
```

**4. Content workflow**
```
Naveesh: "Draft a new post about Proxmox networking"
  → I create draft markdown file with proper frontmatter
  → I run AI-tells detection script
  → I commit to `draft/proxmox-networking`
  → CI validates (types, markdown, links)
  → When ready, I set `draft: false` and open PR
```

### What OpenClaw Does NOT Do

- **No visual editor/design tool** — I work in code, not a drag-and-drop interface
- **No hosting** — Cloudflare Workers handles that
- **No CMS dashboard** — content is markdown files in git, editing is via git

But the agent-based workflow (sub-agents for expertise + screenshot previews + iterative feedback loop) is more powerful than any single design tool for this kind of project.

---

## Recommended Next Actions (from research)

| Priority | Action | Why |
|---|---|---|
| 1 | **Container queries** for blog index cards | Cards adapt to available space without media query hacks |
| 2 | **Per-post OG images** via Satori/Astro | Makes shared links actually look good on X/Slack/Discord |
| 3 | **Next/previous post links** | Low-effort, high-engagement improvement |
| 4 | **PageFind search** | Essential before 20 posts — easier to add now |
| 5 | **`text-wrap: pretty`** on body content | Prevents orphan words, zero cost |
| 6 | **Image dimensions in markdown** | Prevents layout shift during loading |
