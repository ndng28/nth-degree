# Blog Design Inspiration — nth degree

## Astro Templates (Could Fork or Steal Ideas From)

### 1. astro-zen-blog — larry-xue/astro-zen-blog
- **Vibe:** Minimal, zen, clean
- **Features:** Dark mode, local search, tag system, RSS, social links, SEO
- **Live demo:** https://blog.larryxue.dev/
- **Takeaway:** Clean config file for site settings, social media links in header, search built-in
- **Why relevant:** Most similar to nth degree's design direction

### 2. astro-tech-blog — nicdun/astro-tech-blog
- **Vibe:** Crisp tech blog with Tailwind
- **Features:** RSS, syntax highlighting, SEO, Vercel deployment
- **Takeaway:** Uses rehype-pretty-code for beautiful code blocks, sitemap integration
- **Why relevant:** Tech-focused, similar audience

### 3. minimal — ekmas/minimal
- **Vibe:** Ultra-minimal, content-first
- **Features:** View Transitions API, Expressive Code code blocks, Shiki, dark/light toggle, content collections
- **Live demo:** https://ekmas.minimal.pages.dev/
- **Takeaway:** Uses `@astrojs/view-transitions` for smooth SPA-like navigation. Code blocks styled with expressive-code.
- **Why relevant:** Shares our "no fluff" philosophy

### 4. northendlab-light-astro — themefisher/northendlab-light-astro
- **Vibe:** Professional blog with 10+ pages
- **Features:** OG images, contact form, author pages, category system, Tailwind, draft posts
- **Takeaway:** OG image support built-in, category system for content organization
- **Why relevant:** More feature-rich, good for understanding what a "complete" blog template looks like

### 5. paperastro — fabformhub/paperastro
- **Vibe:** Paper-like, reading-focused
- **Takeaway:** Content-first design, minimal chrome
- **Why relevant:** Reading-focused aesthetic

### 6. astro-zero — protomorph/astro-zero
- **Vibe:** Zero styling starting point
- **Features:** MDX, simple structure
- **Takeaway:** Starting from zero lets you build exactly what you want

---

## Real Engineering Blogs (Design Study)

### 7. overreacted.io — Dan Abramov
- **What to study:** Ultra-minimal. White bg, black text, narrow column. Zero chrome. The content IS the design.
- **What to steal:** Narrow column (650px), generous leading (1.8), total lack of decoration
- **Stack:** Gatsby + MDX (but design is framework-agnostic)

### 8. joshwcomeau.com — Josh W Comeau
- **What to study:** Gorgeous interactive design. CSS gradients, smooth transitions, interactive code blocks. Shows what's possible with a design-forward engineering blog.
- **What to steal:** Code block design (language labels, copy button, hover effects), rainbow accent colors, playful but not unprofessional
- **Note:** Opposite end of the spectrum from nth degree's minimal ethos — but the code block UX is best-in-class

### 9. leerob.io — Lee Robinson
- **What to study:** Clean, modern, professional. Vercel engineer's personal site.
- **What to steal:** Home page layout (hero intro → featured projects → latest posts), clean nav, OG image pattern

### 10. stratechery.com — Ben Thompson
- **What to study:** Premium long-form tech analysis. Paid subscription model. Typography is pristine.
- **What to steal:** The sense of editorial authority. The typography is doing the work — nothing fancy, just perfectly tuned.

### 11. matt-rickard.com — Matt Rickard
- **What to study:** Minimal engineering blog. Home page is just a list of posts. No images, no fluff.
- **What to steal:** The commitment to minimalism. Every post starts with the content — no hero, no featured image, just writing.

### 12. boringavocado.com
- **What to study:** Clean engineering blog with good typography. Dark mode with warm accents.
- **What to steal:** Color palette (warm dark mode), tag system, post layout

### 13. gwern.net — Gwern Branwen
- **What to study:** Extreme density. Perfect typography for long-form technical content. Reference-style linking.
- **What to steal:** Side annotations, reference footnoting, the idea that a personal site can be a serious research publication

---

## Design Pattern Library (for specific elements)

### 14. Stripe Docs (docs.stripe.com)
- **What to study:** Code blocks. Best-in-class developer documentation with clean, readable code samples. Syntax highlighting that's actually pleasant to read.

### 15. Vercel Blog (vercel.com/blog)
- **What to study:** Card patterns, hero simplicity, reading progress indicator. Their blog is a masterclass in "designed but minimal."

### 16. Daring Fireball (daringfireball.net)
- **What to study:** The original minimal blog. John Gruber's site proves you can have a hugely successful blog with almost no design — as long as the writing is good.

---

## What I Recommend Borrowing

These are the specific ideas I'd pull from these references:

| Element | Source | Why It Fits nth degree |
|---------|--------|----------------------|
| **Code block design** | Josh Comeau / Stripe | Language label, copy button, clean highlighting |
| **Home page layout** | leerob.io | Hero → featured post → recent list (close to what we have) |
| **Narrow, focused column** | overreacted.io | 650-740px, no sidebar, no distractions |
| **Search** | astro-zen-blog | Local search with PageFind (zero JS overhead) |
| **OG images** | northendlab + leerob | Generate at build time per post |
| **View transitions** | ekmas/minimal | Smooth page nav with Astro's ViewTransitions API |
| **Tag/category system** | northendlab | More structured content organization |
| **Warm dark mode** | boringavocado | Our current palette is good but could be warmer |
| **Reading progress** | Vercel blog | Already done via CSS |

---

## Not Recommended

- **Tailwind CSS** — Adds build complexity, conflicts with our "zero framework" philosophy. Our custom CSS is leaner.
- **Client JS frameworks** (React/Vue/Svelte) — Violates the existing no-JS constraint. Astro islands pattern could work for specific components (search modal, dark mode toggle) but keep it minimal.
- **Heavy animations** — Engineering blogs don't need scroll-triggered fade-ins or parallax. They need readable text.
- **Sidebars** — Don't add a sidebar. Our single-column layout is correct for a content-focused blog.
