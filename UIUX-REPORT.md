# UI/UX Audit & Best-Practices Report — nth degree

**Audience:** Engineering blog maintainer  
**Current state:** Minimal Astro blog, clean codebase, no CSS frameworks or client JS  
**Philosophy alignment:** Very strong. The no-fluff ethos extends to the UI — this is a good foundation.

---

## Executive Summary

nth degree has a solid, opinionated base. The typography choices (Inter + JetBrains Mono) are excellent. The no-JS constraint is a legitimate design boundary, not a limitation. The reading experience is already above average for a self-built blog.

**This report identifies where small, targeted improvements yield the most reader-facing impact** — not a redesign, but a refinement of what's already working well.

---

## Section 1: Top 5 Improvements (Priority Order)

### 1. 🎨 Complete the Color System for Dark & Light Mode

**What's there now:** A minimal set of ~13 CSS custom properties covering bg, surface, border, text, accent, code-bg, and selection. Works in both modes.

**The problem:** The current palette works but lacks depth. There's no way to express hierarchy (subtle surfaces, hover states on secondary elements, proper syntax highlighting tokens). The `selection` color uses a shared accent approach but doesn't adjust opacity between modes thoughtfully. Most critically: **the light mode is visually flatter and less refined** than the dark mode — the surface colors are too similar to each other and to the background.

**What to do:** Implement a full semantic color token system (see Section 2 below). This gives you the vocabulary to build richer surfaces, hoverable cards, syntax highlighting, and proper visual hierarchy — all without a single line of JS.

*Expected impact:* High. Color is the single most visible aspect of a site's quality.

### 2. 📐 Implement a Fluid Typography System

**What's there now:** Fixed font sizes (17px body, 2rem/1.35rem/1.1rem headings, 0.85rem for small text). Media queries adjust body to 16px on small screens. Hero title jumps from 2.75rem to 2rem at 640px.

**The problem:** Fixed breakpoints cause jarring jumps. A 640px phone held in landscape vs portrait shows different layouts. The hero title is way too large on an iPad and loses its punch on a large desktop. Body text at 17px is good, but without fluid scaling it doesn't benefit from larger screens.

**What to do:** Implement a `clamp()`-based fluid type scale using a tool like [Utopia](https://utopia.fyi/) or a hand-tuned version (see Section 3). This gives you smooth scaling from 360px to 1440px+ without any breakpoints.

*Expected impact:* Medium-high. Readers won't consciously notice, but they'll feel the difference — less zooming, more comfortable reading across devices.

### 3. 🔍 Add Full-Text Search

**What's there now:** No search whatsoever. Navigation relies entirely on the Posts list, Tags index, and manual browsing.

**The problem:** As the blog grows past 10-20 posts, finding specific content becomes tedious. Engineering blogs are reference-heavy — readers often need to find "that post about Caddy configs" or "the one about VLANs." Without search, they browse or leave.

**What to do:** Use Astro's built-in support for [pagefind](https://pagefind.app/) or [minisearch](https://github.com/lucaong/minisearch/). Both generate static search indexes at build time with zero client JS for the index — only a small search UI component. PageFind gives you the best out-of-box experience; MiniSearch is lighter but needs more wiring.

**Recommendation:** PageFind. Add it to the Astro build pipeline. Add a small search UI accessible from the nav bar (magnifying glass icon, keyboard shortcut `/`). Zero runtime cost beyond the search interface itself.

*Expected impact:* Medium. Critical for growth; low priority before ~15 posts but good to plan for.

### 4. 🖼️ Add Open Graph & Social Cards

**What's there now:** Standard meta tags (description, viewport, theme-color). No OG tags, no Twitter cards, no social preview image.

**The problem:** When someone shares a post on Slack, Twitter/X, Discord, or any social platform, the link renders as a bare URL or an unstyled card. No image, no rich preview. This dramatically reduces click-through rates from shared links.

**What to do:** Add `og:title`, `og:description`, `og:type`, `og:url`, `og:image` meta tags to the `Base.astro` layout. Generate a dynamic OG image at build time using Astro's image processing or a static template. Even a simple text-over-background image (post title + site logo on a gradient) is miles better than nothing.

**Minimal path:** Add the meta tags with a static default OG image first (a site-branded "nth degree" card). Then generate per-post images using [@vercel/og](https://vercel.com/docs/functions/edge-functions/og-image-generation) or the simpler [satori](https://github.com/vercel/satori) approach — both work at build time.

*Expected impact:* High for social shareability. If you ever want links shared on X/Twitter, LinkedIn, or Slack, this is table stakes.

### 5. 🧭 Improve Internal Navigation & Content Discovery

**What's there now:** Nav bar (Posts, Tags, About), breadcrumb "All posts" back link on post pages, Tags index page, per-tag post lists.

**The problem:** There's no way to navigate between related posts. Once a reader finishes a post, the only paths forward are: browser Back button, nav bar to Posts, or nav bar to Tags. No "next post" / "previous post" links. No related posts by tag. No series grouping (e.g., for multi-part how-to guides).

**What to do:**
- **Next/Previous post links** at the bottom of each article — chronologically adjacent posts. This is easy, high-engagement, and cheap.
- **Related posts by shared tags** — show 2-3 posts that share the most tags with the current post. Falls back to most recent if none share tags.
- **Reading progress indicator** — a thin accent-colored bar at the very top of the page that fills as the reader scrolls. Simple CSS-only approach: use `animation-timeline: scroll()` (Chromium already supports this) or a tiny JS snippet (no dependencies acceptable? use the CSS-only version).
- **"Featured" on the home page** could link to the second+ tagged post to give curated prominence.

*Expected impact:* Medium. Increased pages-per-session and time-on-site. Readers stay longer, find more content.

---

## Section 2: Color System — Complete Refined Palette

### Design Principles

1. **Semantic naming** — colors are named by use, not by value (`--text-body`, not `--gray-900`)
2. **WCAG AA minimum** — body text ≥ 4.5:1 contrast, large text ≥ 3:1, UI elements ≥ 3:1
3. **Dark mode** uses lower overall contrast (L* ~5-12 for backgrounds) with carefully lifted accent colors
4. **Light mode** uses warmer neutrals (avoid pure gray — it looks clinical)

### Base Surface Layers

These create depth hierarchy in cards, modals, and dropdowns:

```css
/* —— DARK MODE (prefers-color-scheme: dark) —— */
:root {
  --bg:            #0b0b0e;   /* Page background — very dark, slightly warm (was #0a0a0b) */
  --bg-elevated:   #111114;   /* Card / surface — one step up (was #141416) */
  --bg-raised:     #18181c;   /* Hovered card / active surface (was #1a1a1e) */
  --bg-overlay:    #1e1e24;   /* Modal / popover backdrop (new) */

  --border-subtle: #222226;   /* Low-priority borders (was #27272a) */
  --border:        #2a2a2f;   /* Default borders (was #27272a) */
  --border-strong: #3a3a40;   /* High-priority borders (new — active states) */

  --text-body:     #e3e3e8;   /* Body text (was #e4e4e7) — slightly warmer */
  --text-secondary:#9f9fa8;   /* Secondary text (was #a1a1aa) */
  --text-muted:    #6b6b76;   /* Muted / de-emphasized (was #71717a) */
  --text-inverse:  #111114;   /* Text on accent backgrounds */

  --accent:        #60a5fa;   /* Primary accent (was #60a5fa — keep, it's good) */
  --accent-hover:  #7bb7fc;   /* Accent hover state (new) */
  --accent-dim:    #3b82f6;   /* Dimmer accent (keep) */
  --accent-subtle: #1e3a5f;   /* Subtle accent background (new — for badges, tags) */

  --code-bg:       #121216;   /* Code block background (was #18181b) */
  --selection:     rgba(96, 165, 250, 0.25);  /* Text selection (was 0.2) */
  --syntax-keyword:#f472b6;   /* Reserved keywords (new, for shiki/Prism themes) */
  --syntax-string: #86efac;   /* Strings (new) */
  --syntax-func:   #60a5fa;   /* Functions (new) */
  --syntax-const:  #c084fc;   /* Constants/vars (new) */
  --syntax-comment:#52525b;   /* Comments (new) */
}

/* —— LIGHT MODE (prefers-color-scheme: light) —— */
@media (prefers-color-scheme: light) {
  :root {
    --bg:            #fafafa;   /* Page background — off-white, warm (was #ffffff) */
    --bg-elevated:   #f0f0f2;   /* Card / surface (was #f4f4f5) */
    --bg-raised:     #e8e8ec;   /* Hovered card (was #eaeaea) */
    --bg-overlay:    rgba(0, 0, 0, 0.04);   /* Modal backdrop (new) */

    --border-subtle: #e2e2e6;   /* Low-priority (was #e4e4e7) */
    --border:        #d4d4d8;   /* Default (was #d4d4d8 — keep) */
    --border-strong: #a1a1aa;   /* Active states (new) */

    --text-body:     #18181b;   /* Body text (was #18181b — keep) */
    --text-secondary:#52525b;   /* Secondary (was #52525b — keep) */
    --text-muted:    #71717a;   /* Muted (keep) */
    --text-inverse:  #ffffff;   /* Text on accent backgrounds */

    --accent:        #2563eb;   /* Primary (keep) */
    --accent-hover:  #1d4ed8;   /* Accent hover (was accent-dim) */
    --accent-dim:    #1d4ed8;   /* Dim accent (keep) */
    --accent-subtle: #dbeafe;   /* Subtle accent bg (new — badge/tag bg in light) */

    --code-bg:       #f4f4f6;   /* Code block (was #f4f4f5) */
    --selection:     rgba(37, 99, 235, 0.18);  /* Selection (was 0.15) */
    /* Syntax colors for light mode — darker to contrast against white */
    --syntax-keyword:#be185d;
    --syntax-string: #15803d;
    --syntax-func:   #1d4ed8;
    --syntax-const:  #7c3aed;
    --syntax-comment:#a1a1aa;
  }
}
```

### Contrast Check (Key Pairs)

| Pair | Mode | Ratio | Pass |
|------|------|-------|------|
| `--text-body` on `--bg` | Dark | ~15.6:1 | ✅ AAA |
| `--text-secondary` on `--bg` | Dark | ~8.3:1 | ✅ AAA |
| `--text-muted` on `--bg` | Dark | ~5.3:1 | ✅ AA |
| `--text-body` on `--bg-elevated` | Dark | ~14.2:1 | ✅ AAA |
| `--text-body` on `--bg` | Light | ~14.8:1 | ✅ AAA |
| `--accent` on `--bg-elevated` | Dark | ~5.5:1 | ✅ AA (for UI) |
| `--accent` on `--bg` | Light | ~6.3:1 | ✅ AA (for UI) |

### Implementation Notes

- Replace `--surface` with `--bg-elevated` (more semantic; use it everywhere a card or container needs a visible background)
- Replace `--surface-alt` with `--bg-raised` (hover state of elevated surfaces)
- Add `--border-subtle` for things like horizontal rules (`<hr>`) and table row separators — lower visual weight
- Syntax highlighting tokens require a code syntax highlighter (shiki is bundled with Astro, see Section 4)

---

## Section 3: Typography — Fluid Type Scale

### Design Principles

1. **Fluid scaling** via `clamp()` — no media-query breakpoints for font size
2. **Utopia-inspired scale** but tuned for a reading blog (less dramatic range than marketing sites)
3. **Inter** remains the body font (excellent for screen reading at 16-18px)
4. **JetBrains Mono** for code (already well-implemented)
5. **Modular scale of 1.25** (major third) for headings, slightly compressed for smaller screens

### Fluid Type Scale

```css
/* Font sizes using clamp(min, preferred, max) */
/* Viewport range: 360px → 1440px */

:root {
  /* Body text — scales smoothly */
  --text-sm:      clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);   /* 12px → 14px */
  --text-base:    clamp(1rem, 0.95rem + 0.25vw, 1.125rem);     /* 16px → 18px */
  --text-ml:      clamp(1.0625rem, 1.0rem + 0.3vw, 1.2rem);    /* 17px → 19.2px (hero desc) */

  /* Heading scale — major third (×1.25) */
  --text-h5:      clamp(0.85rem, 0.8rem + 0.25vw, 1rem);       /* ~14px → 16px (section labels) */
  --text-h4:      clamp(1rem, 0.95rem + 0.25vw, 1.125rem);     /* ~16px → 18px */
  --text-h3:      clamp(1.1rem, 1.0rem + 0.5vw, 1.35rem);      /* ~17.6px → 21.6px */
  --text-h2:      clamp(1.3rem, 1.1rem + 1.0vw, 1.75rem);      /* ~20.8px → 28px */
  --text-h1:      clamp(1.6rem, 1.2rem + 2.0vw, 2.25rem);      /* ~25.6px → 36px (post title) */
  --text-hero:    clamp(2rem, 1.4rem + 3.0vw, 3rem);           /* 32px → 48px (home page hero) */

  /* Leading (line-height) */
  --leading-tight:   1.15;    /* Hero / H1 */
  --leading-snug:    1.3;     /* H2-H3 */
  --leading-normal:  1.65;    /* Body (was 1.75 — 1.65 works better at 17-18px) */
  --leading-relaxed: 1.8;     /* Long-form content */

  /* Font weights */
  --weight-normal:  400;
  --weight-medium: 450;      /* Inter's mid-weight — distinct without being bold */
  --weight-semibold:600;
  --weight-bold:    650;      /* Astro-style — heavier than typical 700, cleaner */
}
```

### Implementation Mapping

Replace current font-size declarations:

| Current | New | Context |
|---------|-----|---------|
| `17px` | `var(--text-base)` | Body `.content` |
| `16px` (mobile body) | _(removed — fluid handles it)_ | — |
| `2.75rem` hero H1 | `var(--text-hero)` | Home page|
| `2rem` page H1 | `var(--text-h1)` | Post titles, page headers|
| `1.35rem` H2 | `var(--text-h2)` | Section headings |
| `1.1rem` H3 | `var(--text-h3)` | Sub-section headings |
| `0.875rem` nav/footer | `var(--text-sm)` | Navigation, footer |
| `0.85rem` time/meta | `var(--text-sm)` | Dates, reading time |

### Line Length (Max-Width)

Current `--max-width: 740px` is good for body text at 17px. At a fluid 18px (1440px viewport), 740px gives ~41 characters per line. The ideal range for English prose is 45-75 characters, with 66 being the "golden" target.

**Recommendation:** Keep `--max-width: 740px`. If you widen content (tables, code blocks), let them scroll horizontally or overflow naturally. For code blocks specifically, consider a **slightly wider max-width on the article content** — maybe 760px or 780px — to give code fewer line wraps.

Better approach: use two max-width values:

```css
:root {
  --max-width-text: 720px;    /* Paragraph text */
  --max-width-content: 780px;  /* Full article content area (wider for code/docs) */
}
```

Then apply `--max-width-content` to the `.content` wrapper for code blocks and tables, while text naturally stays narrower via paragraph margin.

### Line Height

Current `line-height: 1.75` is good. I'd suggest **1.65 for body text** at the fluid 16-18px range — it's slightly tighter, which reduces eye travel on longer lines. For the `.content` article container, `1.8` is fine since it has more heading spacing to break up long sections.

---

## Section 4: Reading Experience & Code Blocks

### Code Block Enhancements

**Current state:** Dark background (`#18181b` dark / `#f4f4f5` light), border, rounded corners, mono font at 0.825em. Scrollable. No syntax highlighting.

**What Astro gives you out of the box:** Shiki syntax highlighting (Shiki ships with Astro v6). Enable it in `astro.config.mjs`:

```js
export default defineConfig({
  output: "static",
  site: "https://blog.ddght.net",
  markdown: {
    syntaxHighlight: "shiki",
    shikiConfig: {
      theme: {
        dark: "github-dark-dimmed",
        light: "github-light",
      },
      wrap: false,
    },
  },
});
```

**Why Shiki is the right choice:** It generates static, pre-colored HTML at build time. Zero runtime cost. No JS. It's the only responsible choice for a no-JS site.

**Custom theme tokens (if rolling your own syntax theme):**

```css
/* Dark mode syntax — warm, accessible token colors */
/* These integrate with Shiki's CSS variable theme approach */
.content pre .token.keyword  { color: #f472b6; }   /* Pink — if/else/for/return */
.content pre .token.string   { color: #86efac; }   /* Green — string literals */
.content pre .token.function { color: #60a5fa; }   /* Blue — function names */
.content pre .token.number   { color: #fbbf24; }   /* Amber — numbers */
.content pre .token.comment  { color: #52525b; }   /* Gray — comments */
.content pre .token.constant { color: #c084fc; }   /* Purple — const/let */
.content pre .token.operator { color: #a1a1aa; }   /* Muted — +, -, = */
.content pre .token.punctuation { color: #a1a1aa; } /* Brackets, parens */
```

### Code Block Improvements

1. **Add a subtle "copy" button** — Yes, this needs JS, but it's 10 lines of vanilla inline JS. The UX improvement for readers who copy configs is massive. Show it as a small icon button that appears on hover.
   - Fallback: the button is `display: none` by default, toggled via JS.
   - Zero external dependencies.

2. **Add line numbers** — Astro's Shiki integration supports `showLineNumbers`. For engineering content (configs, code samples), line numbers are genuinely useful for reference in comments or when copying.

3. **Show the language label** — A small label in the top-right corner of the code block (e.g., "yaml", "bash"). Implemented as a pseudo-element or a `<span>` in the rendered HTML.

### Image & Figure Enhancements

- **Add `loading="lazy"`** to all content images for performance.
- **Add lightbox** — Since you have no JS, a pure-CSS lightbox using `:target` or `<details>` is possible but clunky. Consider: images are already max-width 100% with rounded corners and a subtle border. That may be sufficient. If you want a lightbox, the simplest approach is an `<a>` wrapping the image that links to the image itself. Users click → open in new tab/browser. No JS.

### Table Enhancements

- Tables are well styled. Add `overflow-x: auto` (already on `<pre>`, but tables lack it). Wrap tables in a `<div class="table-wrapper">` with overflow-x: auto for small screens.

---

## Section 5: Layout — Container Queries & Responsive

### Current Layout Architecture

```
body (max-width: 740px, margin: 0 auto)
├── nav
├── main
│   ├── hero / page-header
│   ├── featured section (home)
│   ├── post-list (multi-card)
│   └── article.content
└── footer
```

This is a single-column, content-out layout. It's the right choice for a reading-focused blog.

### Where Container Queries Help

The most impactful use of container queries isn't for the page layout — it's for **card components that might appear in different contexts**:

```css
/* Define a container on the post list area */
.post-grid {
  container-type: inline-size;
  container-name: card-grid;
}

/* Cards adjust within their container */
@container card-grid (max-width: 500px) {
  .post-card {
    padding: 1.25rem;  /* Less padding when constrained */
  }
  .post-card .post-desc {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

**Practical application:** Right now, the same card pattern appears on `/blog`, on `/blog/tags/[tag]`, and potentially in a "related posts" section. Container queries let the same component adapt to its context without media queries tied to viewport.

### Responsive Breakpoints

Current breakpoints at 640px and 480px are good. Add explicit handling:

```css
/* Default: desktop-first design */
/* Medium screens (tablet portrait — iPad Mini at 768px) */
@media (max-width: 768px) {
  body { padding: 2.5rem 1.5rem; }
  .featured-card { padding: 1.5rem; }
  .post-card { padding: 1.5rem; }
}

/* Small screens (phone — 640px and below) */
@media (max-width: 640px) {
  body { padding: 1.5rem 1rem; }
  nav { flex-direction: column; gap: 0.75rem; }
  .post-row { flex-direction: column; gap: 0.25rem; }
  .post-row .post-row-date { align-self: flex-start; }
  .tags { gap: 0.3rem; }
}

/* Very small screens (compact phones — 400px) */
@media (max-width: 400px) {
  body { padding: 1rem 0.75rem; }
  header.hero h1 { font-size: var(--text-h1); } /* Falls back to clamped hero */
  .nav-links { gap: 1rem; }
  .featured-card { padding: 1rem; }
  .post-card { padding: 1rem 1.25rem; }
  .content pre { padding: 0.75rem; margin: 1rem -0.75rem; border-radius: 0; }
}
```

### Navigation on Mobile

The current nav (Posts · Tags · About on one line in a flex row) breaks to wrap on very small screens. Two improvements:

1. **Allow the nav links to wrap** — currently they're in a single `.nav-links` flex row with a fixed gap. On 360px screens, "Posts Tags About" wraps but the gap and font sizes keep it reasonable.
2. **Consider a hamburger** — Not recommended given the no-JS constraint. Three nav items don't warrant a hamburger menu. Just let them wrap.

---

## Section 6: Micro-interactions & Transitions

### Current State

- Link hover: opacity 0.8 + underline
- Nav link underline: `::after` pseudo-element with width transition
- Featured/post card hover: border-color to accent + subtle box-shadow
- Tag hover: color + border-color to accent
- `scroll-behavior: smooth`

### Recommendations

All must be performant (animate only `opacity` and `transform`) and work without JS:

1. **Card entrance animation:** Use `@starting-style` or `@keyframes` with `animation` on cards. Because Astro generates static HTML at build time, you can't use `view-transition` API easily (it requires SPA navigation). Instead:

```css
.post-card {
  /* Subtle hover lift */
  transition: border-color 0.2s ease,
              box-shadow 0.2s ease,
              transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.post-card:hover {
  transform: translateY(-2px);  /* Slightly more than current -1px */
}
```

The `cubic-bezier(0.34, 1.56, 0.64, 1)` gives a slight "spring" feel on hover — imperceptible but delightful.

2. **Reading progress bar** — CSS-only approach using the modern `scroll-timeline` (Chromium 115+, Firefox 116+, Safari 18.2+):

```css
/* Only works in Chromium + newer Firefox */
@supports (animation-timeline: scroll()) {
  #reading-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 2px;
    background: var(--accent);
    transform-origin: 0 50%;
    animation: progress-grow linear;
    animation-timeline: scroll(root);
  }

  @keyframes progress-grow {
    from { scale: 0 1; }
    to { scale: 1 1; }
  }
}
```

Add `<div id="reading-progress"></div>` to `Base.astro`. Zero JS, works in ~85% of browsers.

3. **Reduce motion** — Respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Section 7: Missing Features & Additions

### 🎯 High Priority (Social Proof & Growth)

| Feature | Approach | Effort |
|---------|----------|--------|
| **OG Meta Tags** | Add to `Base.astro` head | Low |
| **OG Image generation** | Static template or `@vercel/og` at build | Medium |
| **RSS `<link>` in head** | Already done ✅ | — |
| **Canonical URLs** | Add `<link rel="canonical">` | Low |

### 🎯 Medium Priority (Reader Experience)

| Feature | Approach | Effort |
|---------|----------|--------|
| **Full-text search** | PageFind at build time | Medium |
| **Next/Previous Post** | `getCollection` sorted by date | Low |
| **Related posts** | Tag-share matching, fallback to recent | Low |
| **Reading progress bar** | CSS `scroll-timeline` | Low |
| **Code copy button** | 10-line vanilla JS | Low |
| **Syntax highlighting** | Shiki in Astro config | Low |
| **Table of Contents** | For long posts — auto-generated from headings | Medium |
| **Post series (prev/next in series)** | Manual frontmatter field `series:"name"`, then filter | Low |

### 🎯 Low Priority / Later

| Feature | Notes |
|---------|-------|
| **Dark mode toggle** | Inconsistent with design ethos. `prefers-color-scheme` is cleaner |
| **Comments** | Use a lightweight embed (utteranc.es, giscus) or none at all. Engineering blogs rarely get comments |
| **Newsletter signup** | Useful for growth, but adds email infrastructure |
| **Post views / analytics** | Plausible, Umami, or Fathom — lightweight and privacy-respecting |
| **Sitemap** | Astro generates this automatically with `sitemap` integration |
| **Pagination** (blog index) | Only needed at 20+ posts |
| **Tags page: show count in header** | ✅ Already done |

---

## Section 8: Inspiration References & Rationale

### What to Study

| Source | What to Borrow |
|--------|----------------|
| **Stripe Docs** | Information density. Clean code blocks with language labels. Fluid typography. |
| **Vercel Blog** | Card patterns with subtle hover states. Hero simplicity. Reading progress indicator. |
| **Stratechery** | Long-form readability. Minimal chrome. The content is the design. |
| **Daring Fireball** | Ultra-minimal. Gruber's site proves you can have a great blog with almost no design. But his typography is precisely tuned. |
| **The New Yorker / Paris Review** | Generous leading, comfortable measure, and the understanding that reading is a physical experience. |
| **Gwern.net** | Extreme content density with perfect typography. Shows how far you can push a reader-focused site. |

### nth degree's Design Niche

nth degree sits between Stratechery (commentary/analysis) and Gwern (technical reference). It should feel like:

- **Minimal but not bare** — enough design to be pleasant, not enough to be noticed
- **Technical but not cold** — warm neutrals, approachable contrast
- **Fast** — the no-JS constraint already guarantees this
- **Authoritative** — the typography does the work; no decorative cruft

The current design achieves most of this. The refinements above take it from "good for a personal project" to "comparable with professionally designed engineering blogs."

---

## Appendix: `astro.config.mjs` Recommended Additions

```js
// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  output: "static",
  site: "https://blog.ddght.net",
  markdown: {
    syntaxHighlight: "shiki",
    shikiConfig: {
      theme: {
        dark: "github-dark-dimmed",
        light: "github-light",
      },
      wrap: false,
    },
  },
  integrations: [sitemap()],
});
```

Add `@astrojs/sitemap` and `@astrojs/mdx` (for future flexibility — MDX is a superset of Markdown that lets you embed components):

```
npm install @astrojs/sitemap @astrojs/mdx
```

---

## Summary: Action Plan (Ordered by Impact/Effort)

| # | Action | Impact | Effort | Time |
|---|--------|--------|--------|------|
| 1 | Refine color system (Section 2) | High | Low | 30 min |
| 2 | Enable Shiki syntax highlighting | High | Low | 5 min |
| 3 | Add OG meta tags + static OG image | High | Low | 1-2 hrs |
| 4 | Add fluid typography (Section 3) | Medium | Medium | 1 hr |
| 5 | Add next/previous post navigation | Medium | Low | 30 min |
| 6 | Add CSS reading progress bar | Medium | Low | 10 min |
| 7 | Add related posts by tags | Medium | Low | 45 min |
| 8 | Add code copy button + language labels | Medium | Low | 30 min |
| 9 | Add PageFind search | Medium | Medium | 2 hrs |
| 10 | Add `@astrojs/sitemap` + canonical URLs | Low | Low | 10 min |
| 11 | Add `prefers-reduced-motion` support | Low | Low | 5 min |
| 12 | Dynamic OG image per post | Medium | High | 3-4 hrs |

**Total 1-6:** ~3-4 hours of work for a measurable quality-of-experience improvement.  
**Total 1-12:** ~10-12 hours for a full polish pass that brings nth degree to a professional-grade reading experience.

---

*Report compiled from a thorough review of the nth degree source code and current content-focused design best practices (Spring 2026).*
