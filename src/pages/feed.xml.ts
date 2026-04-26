import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const GET: APIRoute = async ({ site }) => {
  const posts = await getCollection("blog");
  const published = posts
    .filter((p) => !p.data.draft)
    .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf());

  const siteUrl = site?.href ?? "https://nth-degree.com";

  const items = published
    .map(
      (post) => `
    <entry>
      <title>${escapeXml(post.data.title)}</title>
      <link href="${siteUrl}blog/${post.id}/"/>
      <published>${post.data.publishDate.toISOString()}</published>
      <id>${siteUrl}blog/${post.id}/</id>
      <summary type="html">${escapeXml(post.data.description)}</summary>
    </entry>`
    )
    .join("\n");

  const feed = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>nth degree</title>
  <subtitle>Engineering depth from a homelab portfolio</subtitle>
  <link href="${siteUrl}feed.xml" rel="self"/>
  <link href="${siteUrl}"/>
  <updated>${published[0]?.data.publishDate.toISOString() ?? new Date().toISOString()}</updated>
  <id>${siteUrl}</id>
  <author>
    <name>naveesh</name>
  </author>
  ${items}
</feed>`;

  return new Response(feed, {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
      "Cache-Control": "max-age=3600",
    },
  });
};

function escapeXml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}
