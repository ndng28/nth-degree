// @ts-check
import { defineConfig } from "astro/config";

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
});