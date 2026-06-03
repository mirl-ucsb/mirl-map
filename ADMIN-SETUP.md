# Content admin (Decap CMS)

mirl-map ships an optional **`/admin`** page where people add photographs,
captions, and narratives in a real editor (drag-drop a photo, type a caption,
write the narrative with live preview, **Publish**) — no code, no token. It is
[Decap CMS](https://decapcms.org), loaded from a CDN. Editors log in with
GitHub; their changes are committed to the repo, and a GitHub Action rebuilds
the site's data and image tiers automatically.

```
/admin  →  edit  →  commit to content/photos/*.md  →  "Build content" Action
        →  regenerates js/data/photos.js + narratives + web/thumb tiers
        →  GitHub Pages redeploys  →  live
```

Only people with **write access to the repo** can save changes (GitHub
permissions are the access control).

---

## Try it locally first (no setup)

You can run the whole CMS against your local files with no login:

```bash
npx decap-server          # in one terminal (starts a local backend on :8081)
python3 -m http.server 8766   # in another
```

Open <http://localhost:8766/admin/>, click **Login**, and edit. This writes to
your working copy; commit/push when you like. Great for trying it before doing
the one-time GitHub login setup below.

---

## One-time setup for "Login with GitHub"

A static host (GitHub Pages) cannot perform GitHub's OAuth secret exchange, so
the login needs one small token-exchange backend. Pick **one** path.

### Path A — stay on GitHub Pages + a Cloudflare Worker (recommended)

1. **Register a GitHub OAuth App**: GitHub → *Settings → Developer settings →
   OAuth Apps → New OAuth App*.
   - Homepage URL: `https://YOUR-USER.github.io/mirl-map/`
   - Authorization callback URL: `https://YOUR-WORKER.workers.dev/callback`
   - Save the **Client ID** and generate a **Client Secret**.
2. **Deploy the OAuth proxy** as a free Cloudflare Worker. Decap documents
   ready-made proxies — see *Decap docs → Backends → GitHub → "External OAuth
   Clients."* Deploy one, and set `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`
   (from step 1) as the Worker's secrets. Note the Worker's URL.
3. **Point the CMS at it** in [`admin/config.yml`](admin/config.yml):
   ```yaml
   backend:
     name: github
     repo: YOUR-USER/mirl-map        # your owner/repo
     branch: main
     base_url: https://YOUR-WORKER.workers.dev
   ```
   Commit and push.
4. **Turn on Pages**: repo *Settings → Pages → Source: GitHub Actions* (the
   included `static.yml` workflow deploys the site).
5. Visit `https://YOUR-USER.github.io/mirl-map/admin/` and click **Login with
   GitHub**.

### Path B — host on Netlify (no Worker, less code)

Netlify can provide the GitHub OAuth for Decap with no proxy of your own.
Deploy the same static files to Netlify, then follow *Decap docs → Backends →
GitHub* for the Netlify OAuth setup (you still register a GitHub OAuth App, with
the callback `https://api.netlify.com/auth/done`). This trades GitHub-Pages
hosting for one fewer moving part.

---

## How editors use it

1. Go to `/admin`, **Login with GitHub**.
2. **Photographs → New Photograph.** Drag in the image, type a **Caption**,
   optionally write the **Narrative** (cite sources with tokens like `[SAMP]`).
   Leave Latitude/Longitude/Bearing/etc. blank — they are read from the photo's
   EXIF automatically.
3. **Publish.** Within a minute the "Build content" Action regenerates the data
   and thumbnails and the live map updates.

To edit an existing photo, open it in the Photographs list, change the caption
or narrative, and Publish.

---

## What's happening under the hood

- The CMS edits one Markdown file per photo in **`content/photos/*.md`** — this
  is now the **source of truth** for photographs.
- **`.github/workflows/build-content.yml`** runs **`scripts/build_content.py`**,
  which compiles those files into `js/data/photos.js`, the `narratives/*.md`,
  and the `photos/web` + `photos/thumb` tiers (filling coordinates, bearing,
  FOV, and capture time from EXIF). Those are **generated** — don't hand-edit
  them; edit the photo in `/admin` or its `content/photos/*.md` instead.
- The command line still works too: `python3 add_photo.py photos/x.jpg` creates
  a `content/photos/` entry and rebuilds.
