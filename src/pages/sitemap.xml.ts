import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const GET: APIRoute = async ({ site }) => {
  const posts = await getCollection("blog");
  const published = posts
    .filter((p) => !p.data.draft)
    .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf());

  const siteUrl = (site?.href ?? "https://blog.ddght.net").replace(/\/$/, "");

  const pages = [
    { loc: "/", priority: "1.0" },
    { loc: "/blog", priority: "0.9" },
    { loc: "/about", priority: "0.7" },
    { loc: "/blog/tags", priority: "0.6" },
  ];

  const entries = [
    ...pages.map(
      (p) => `
  <url>
    <loc>${siteUrl}${p.loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>${p.priority}</priority>
  </url>`
    ),
    ...published.map(
      (post) => `
  <url>
    <loc>${siteUrl}/blog/${post.id}/</loc>
    <lastmod>${post.data.updatedDate?.toISOString() ?? post.data.publishDate.toISOString()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>`
    ),
    ...Array.from(new Set(published.flatMap((p) => p.data.tags))).map(
      (tag) => `
  <url>
    <loc>${siteUrl}/blog/tags/${tag}/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>`
    ),
  ];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${entries.join("")}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "max-age=3600",
    },
  });
};
