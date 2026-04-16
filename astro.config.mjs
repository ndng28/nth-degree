// @ts-check
import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  output: "static",
  site: "https://blog.ddght.net",
  // Content collections validated at build time
  // schema defined in src/content/config.ts
});