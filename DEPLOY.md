# Deploying the LNJC Insights blog

This folder (`blog-site/`) is a **complete, self-contained static website** — no
build step, no server. It's optimized for both traditional SEO and GEO
(discoverability by AI answer engines). Point a static host at this folder and
it's live.

## What's inside

```
blog-site/
├── index.html                 ← blog home (Organization + Blog schema)
├── en/                        ← 2 English posts (for manufacturers)
├── ar/                        ← 3 Arabic posts (for the Yemeni market)
├── assets/blog.css            ← shared styles (RTL-aware, light/dark)
├── assets/*.png               ← logo + OG social cards (see "Replace images")
├── sitemap.xml                ← all 6 URLs
├── robots.txt                 ← allows Google + AI crawlers, points to sitemap
└── llms.txt                   ← GEO: a map of the site for LLM crawlers
```

Every page carries: unique title + meta description, canonical, Open Graph,
**JSON-LD** (`BlogPosting` + `FAQPage` + `BreadcrumbList`, plus `Organization`
on the home page), citations as structured data, and an on-page FAQ. This is
exactly what Google rich results **and** AI answer engines read.

## Before you deploy

1. **Decide the base URL.** Everything is written for **`https://blog.landcarenj.com`**.
   If you use a different domain/subdomain, find-and-replace `blog.landcarenj.com`
   across all files (canonicals, OG URLs, sitemap, JSON-LD `@id`s, llms.txt).
2. **Replace the placeholder images.** `assets/lnjc-logo.png` is your real logo
   (good to keep). The six `assets/og-*.png` are **placeholders** (currently a
   copy of the logo). For proper social/AI previews, replace each with a real
   **1200×630** image. **Imagery is open as of 3 Aug 2026** — photographs,
   illustrations, stock images or designed graphics are all permitted (the
   earlier "LNJC's own photography, no stock" rule was dropped at the client's
   request). Keep the same filenames and nothing else needs to change.
3. **Verify facts once more** — every figure is cited, but confirm the LNJC
   contact details and exclusivity wording against `docs/FACTS.md`, and that the
   Yemen humanitarian figures are still current for your publish date.

## Preview locally (optional)

```bash
cd "blog-site" && python3 -m http.server 8080
```
Then open `http://localhost:8080`. (Root-relative links like `/assets/blog.css`
resolve correctly this way.)

## Publish — pick one host (all free tiers, all serve static folders)

**Option A — Cloudflare Pages** (recommended: fast, free, easy custom domain)
1. Create a Cloudflare account → **Workers & Pages → Create → Pages → Upload assets**.
2. Upload the contents of `blog-site/`.
3. In the project's **Custom domains**, add `blog.landcarenj.com`. Cloudflare
   tells you the DNS record to create.

**Option B — Netlify**
1. Netlify → **Add new site → Deploy manually** → drag the `blog-site/` folder in.
2. **Domain settings → Add a domain** → `blog.landcarenj.com` → follow the DNS step.

**Option C — GitHub Pages**
1. Put `blog-site/` contents in a repo → **Settings → Pages** → deploy from branch.
2. Add `blog.landcarenj.com` as the custom domain.

## DNS (one record, in your domain registrar / Hostinger DNS)

Add a **CNAME**: `blog` → the hostname your chosen host gives you
(e.g. `your-project.pages.dev` or `your-site.netlify.app`). This does **not**
touch your existing `landcarenj.com` site — it only adds the `blog` subdomain.

## After it's live — the SEO + GEO checklist

1. Open `https://blog.landcarenj.com/robots.txt` and `/llms.txt` and `/sitemap.xml`
   — confirm all load.
2. **Google Search Console** → add the `blog.landcarenj.com` property → submit
   `sitemap.xml`.
3. **Bing Webmaster Tools** → import from GSC (also feeds chatbots that use Bing).
4. Test a couple of URLs in Google's **Rich Results Test** — you should see
   Article + FAQ detected.
5. **Link the blog from the main site** (a "Insights/Blog" link on landcarenj.com)
   and link from the blog back to the main site (already done in the footers) —
   internal links consolidate authority and help both properties get crawled.
6. Give it a few weeks; AI answer engines pick up well-sourced, well-structured
   pages like these once they're crawlable.

## Why this instead of the Hostinger builder?

AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) read HTML best
when it's **static and semantic** — a JavaScript single-page builder is the
weakest vehicle for GEO, and can't expose this level of schema. This static
build is also what `docs/SITE.md` already recommends as the long-term direction.
