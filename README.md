# nth degree

Engineering depth from a homelab portfolio.

## Writing

Posts live in `src/content/blog/` as Markdown files with frontmatter:

```yaml
---
title: "Post Title"
description: "One-liner for SEO and listing pages."
publishDate: "2026-04-16"
tags: ["infrastructure", "homelab"]
draft: true
---

Post body here...
```

## Workflow

### Branch model

- `main` — production. CF Pages deploys from here on every push.
- `draft/*` — in-progress posts. Open a PR to `main` when ready to publish.

### Writing a post

```bash
# 1. Switch to a draft branch
git checkout -b draft/my-post-slug

# 2. Create the content file
cat > src/content/blog/my-post-slug.md << 'EOF'
---
title: "My Post"
description: "..."
publishDate: "2026-04-16"
tags: ["topic"]
draft: true
---

Your post content.
EOF

# 3. Stage and commit — this runs the AI tells check
git add src/content/blog/my-post-slug.md
git commit -m "draft: my post title"

# 4. Push and open a PR when ready
git push -u origin HEAD
```

CI validates every push to `draft/*` and every PR to `main`:
- Astro type check + build
- AI tells scan (blocks commit with AI patterns)
- Markdown lint
- Link check (after successful build)

### Publishing

1. Set `draft: false` in frontmatter.
2. PR from `draft/*` to `main`.
3. Merge after CI passes — CF Pages deploys automatically.
4. Purge CDN cache if needed: CF dashboard → Caching → Purge Everything.

### Content guidelines

- Target a single idea per post. Edit ruthlessly.
- No intro that restates the title.
- No bullet-point takeaways at the end.
- Prefer specifics over generalities: "Caddy with a TLS cert from LetsEncrypt" beats "good security."
- Check for AI tells before committing if using an AI writing assistant:
  ```bash
  python3 scripts/check-blog-ai-tells.py --no-install
  ```

## Stack

- **Astro 6** — static site generation with content collections
- **Cloudflare Pages** — hosting and CDN
- **Zod** — frontmatter schema validation at build time
- No CSS frameworks. No JavaScript in the browser.

## Local development

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # production build
npx astro check  # type check
```

## Scripts

- `scripts/check-blog-ai-tells.py` — detects AI-written patterns before commit. Install as pre-commit hook with `python3 scripts/check-blog-ai-tells.py install`.