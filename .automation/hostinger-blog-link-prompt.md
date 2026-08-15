# Prompt: add the blog link to the landcarenj.com navigation

Copy everything inside the box below and paste it into Claude in Chrome, in the Chrome window
where you are already signed in to the Hostinger account that owns landcarenj.com.

Why this matters: blog.landcarenj.com publishes a new article every day and links back to the
main site 34 times, but the main site does not link to the blog even once. Search engines treat
that as two unrelated sites, which is the most likely reason the blog is not appearing in search
results yet. One navigation link fixes it.

---

```
I need you to add one link to the navigation menu of my website in the Hostinger website
builder. Work carefully and do not change anything else on the site.

The site is landcarenj.com. It belongs to LNJC Pharmaceuticals and Medical Supplies, and it is
built with the Hostinger Website Builder, not WordPress. The site has an Arabic version and an
English version.

What I want added:

- On the Arabic version, a new navigation menu item labelled: المدوّنة
- On the English version, a new navigation menu item labelled: Insights
- Both must link to this external address: https://blog.landcarenj.com
- Both should open in a new tab if the builder offers that option
- Place the new item at the end of the existing menu, before any "Contact" item if one exists

Steps:

1. Open hpanel.hostinger.com and find the website landcarenj.com, then open it in the Website
   Builder editor.
2. Find the navigation or header menu settings. In the Hostinger builder this is usually done by
   clicking the header area of the page, then looking for "Manage menu", "Edit menu", or a
   "Pages and navigation" panel in the sidebar.
3. Add a new menu item. Choose the option for an external link or custom link, not a page,
   because the blog is on a separate subdomain and will not appear in the page list.
4. Set the label and the URL exactly as listed above.
5. Repeat for the other language version of the site. In the Hostinger builder, languages are
   switched from a language selector near the top of the editor. Each language has its own menu,
   so adding the item once is not enough.
6. Publish the site.

Before you publish, show me a screenshot of the menu with the new item in it, and tell me
exactly what you changed. After publishing, open https://landcarenj.com in a new tab, confirm
the new menu item appears, click it, and confirm it opens the blog.

Important limits:
- Do not change any other menu item, page, text, image or setting.
- Do not delete anything.
- If the builder will not let you add an external link to the menu, stop and tell me instead of
  working around it. Do not put the link somewhere random.
- If you are asked for a password or any login details, stop and tell me. Do not enter them.
```

---

## If the builder refuses external links in the menu

Some builder templates only allow linking to internal pages. If that happens, the next best
options, in order of value:

1. Add a text link to the site footer pointing at https://blog.landcarenj.com, labelled
   المدوّنة in Arabic and Insights in English. A footer link still passes the signal.
2. Create a thin internal page called "Insights" or "المدوّنة" that contains a short paragraph
   and a prominent link out to the blog, then put that page in the menu.

Option 1 is faster. Option 2 is slightly better for search but takes longer.

## After it is done

Tell Claude Code, and it will confirm the link is live and visible to search engines.

The other two outstanding items, both of which also need you rather than automation:

- Add blog.landcarenj.com to Google Search Console as its own property and submit
  https://blog.landcarenj.com/sitemap.xml
- Get LNJC listed on the trade directories that rank for Yemeni pharmaceutical importers
