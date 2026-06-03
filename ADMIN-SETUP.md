# Setting up the editor, and publishing your map

This is the one part of MIRL Map that is a little technical. Here is the
reassuring part: **you only do it once.** After that, you and anyone you invite
can add photographs, captions, and stories just by filling in a simple web form,
with no files and no code.

If any of the steps below feel unfamiliar, that is completely normal. A colleague
who is comfortable with websites, or the MIRL team, can sit down and do this part
with you. It usually takes about fifteen minutes.

This page covers two things:

1. **Trying the editor on your own computer**, with nothing to set up. A nice way
   to get a feel for it.
2. **Publishing your map online**, so others can see it and help edit it. This is
   the part with the one-time setup.

---

## 1. Try the editor on your own computer (no setup, no accounts)

You can run the whole editor against the copy of the project on your own computer,
with no login and nothing installed permanently. It is a lovely way to see how it
feels before you publish anything.

You will use a program called **Terminal** (it comes with every Mac; on Windows it
is **Command Prompt** or **PowerShell**). It looks plain, but you only need to type
two short lines. Open it, type this, and press Return:

```
npx decap-server
```

Leave that running. Open a second Terminal window and type:

```
python3 -m http.server 8766
```

Now open your web browser at **http://localhost:8766/admin/**, click **Login** (no
password is needed in this local mode), and you are in the editor. Anything you
change is saved to the copy on your computer. Nothing goes online until you decide
to publish.

If those commands look unfamiliar, this is exactly the kind of step a colleague
can run for you once, or you can skip it entirely and go straight to publishing.

---

## 2. Publish your map online

To put your map on the web with a working **Log in with GitHub** button, there is
a short, one-time setup. Here is the plain reason it is needed:

> Your map is simply a set of files, with no computer running behind it. A "Log in
> with GitHub" button needs a private password (a "secret") to complete the login
> safely, and there is nowhere safe to keep that secret inside files that anyone
> can read. So you set up one tiny, free helper that holds the secret and finishes
> the login for you. That is the whole reason for the steps below.

There are two routes. Pick whichever sounds friendlier.

### Route A: keep everything on GitHub, with a small free helper (recommended)

**Step 1. Tell GitHub about your editor.**
On GitHub, go to **Settings**, then **Developer settings**, then **OAuth Apps**,
and click **New OAuth App**. Fill in:

- **Application name:** anything you like, such as "My Map Editor."
- **Homepage URL:** your map's web address, for example
  `https://your-org.github.io/mirl-map/`.
- **Authorization callback URL:** `https://your-helper.workers.dev/callback`. You
  will get this exact address in Step 2, so you can come back and fill it in then.

Click **Register**. GitHub gives you two codes: a **Client ID**, and, after you
click "Generate a new client secret," a **Client Secret**. Keep both handy, and
treat the secret like a password.

**Step 2. Set up the small free helper.**
This is a tiny program that runs for free on **Cloudflare**. You do not have to
write any code: MIRL Map's editor (it is called **Decap**) publishes a ready-made
helper you can use, and the current instructions live on the Decap website under
*Backends, then GitHub, then "External OAuth Clients."* During the setup you paste
in the **Client ID** and **Client Secret** from Step 1. At the end you are given a
web address for your helper, something like `https://your-helper.workers.dev`. Go
back to Step 1 and put its `/callback` address into the GitHub callback box.

**Step 3. Point your map at the helper.**
Open the file `admin/config.yml` in your project and fill in two lines:

```
backend:
  name: github
  repo: your-org/mirl-map                      # your project's name on GitHub
  branch: main
  base_url: https://your-helper.workers.dev    # the address from Step 2
```

Save the change (commit and push it, or edit the file right on github.com).

**Step 4. Turn on the free web hosting.**
In your project on GitHub, go to **Settings**, then **Pages**, and set the source
to **GitHub Actions**. Your map will be published at the Homepage URL from Step 1.

That is everything. Visit `https://your-org.github.io/mirl-map/admin/` and click
**Log in with GitHub.**

### Route B: use Netlify (one less piece to set up)

Netlify is a free hosting service that can handle the GitHub login for you, so you
do not set up the helper yourself. You connect your project to Netlify and follow
Decap's *Backends, then GitHub* instructions for the Netlify login (you still
register a GitHub OAuth App as in Route A, this time with the callback
`https://api.netlify.com/auth/done`). The trade is that your map is hosted by
Netlify instead of GitHub, which is perfectly fine and also free.

---

## Inviting people to edit

Anyone you want to let edit the map needs **permission to the project on GitHub**.
Because your project lives in a GitHub organization (for MIRL, that is
**mirl-ucsb**), members you add with edit access can use the editor straight away.
People without access can still view the published map; they simply cannot change
it.

---

## How your editors use it

1. Go to your map's web address followed by `/admin` (for example
   `https://your-org.github.io/mirl-map/admin/`) and click **Log in with GitHub.**
2. Choose **Photographs**, then **New Photograph.** Drag in the image, type a
   **caption**, and, if you like, write the **narrative.** You can leave the
   location and the other technical boxes empty; they are read from the photograph
   itself.
3. Click **Publish.** Within about a minute, your change appears on the live map.

To change a photograph already on the map, open it from the list, edit it, and
Publish again.

---

## What happens behind the scenes

You do not need to know this, but in case you are curious: each photograph you add
is quietly saved as a small text file, and a helper on GitHub turns your
photographs into the finished map. It also makes the small and medium-sized copies
of each image and reads the location from each photo. You just add photographs and
words; the rest is taken care of for you.

---

## If you get stuck

This setup is honestly the fiddly part, and there is no shame in asking for a
hand. A web-comfortable colleague can usually finish it in one sitting, and the
MIRL team is glad to help.
