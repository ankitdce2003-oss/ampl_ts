# Astranova MOU Generator — Vercel deployment

Same tool as before (web form → filled MOU `.docx`), restructured to run as
a Vercel serverless function.

## Deploy — no coding required

**Option A: via GitHub (recommended, gives auto-deploys on future edits)**

1. Create a new **private** GitHub repo and push this folder's contents to it
   (`api/`, `templates/`, `vercel.json`, `requirements.txt`).
2. Go to https://vercel.com → sign in (GitHub login is easiest) → **Add New → Project**.
3. Import that repo. Vercel auto-detects the Python function — leave settings
   as default and click **Deploy**.
4. After ~30-60s you'll get a URL like `https://astranova-mou.vercel.app`.
   Share that with your team.

**Option B: via CLI, no GitHub needed**

```bash
npm install -g vercel     # one-time
cd vercel_deploy
vercel login
vercel --prod
```

It will print the live URL when done.

## Updating later

- To change form fields or wording: edit `templates/form.html`, then redeploy
  (push to GitHub, or run `vercel --prod` again).
- To update the underlying MOU legal template: replace
  `MOU_source.docx` with the revised file in the main project folder, re-run
  `python3 build_template.py` there, then copy the regenerated
  `MOU_template.docx` into `vercel_deploy/api/MOU_template.docx` and redeploy.

## Notes specific to Vercel

- Free plan functions time out after 10 seconds — generating this docx takes
  well under a second, so this is not a concern.
- There's no persistent server between requests (serverless), so nothing is
  stored between form submissions — each submission is generated fresh,
  which is exactly what you want here.
- If you later want a custom domain (e.g. `mou.astranovamobility.com`)
  instead of the `*.vercel.app` link, that's added under the Vercel
  project's **Settings → Domains**.

---
*This tool auto-fills a standard template for internal drafting purposes
only. Every generated MOU should be reviewed before it is sent externally.*
