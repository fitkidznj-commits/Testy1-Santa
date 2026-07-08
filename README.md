# Hammer Head Group — Social Media Approval Site

A public, unlisted web app for Hammer Head Group to review a 30-day social
media campaign. The client opens one link, reviews each day (image + caption)
plus the 4 weekly highlight videos, and either **Approves** or **Requests
edits** with a note. There's also a **name** and **overall comments** field.

Every decision is stored **centrally on the server** (not just in the
browser), so the agency sees results at a protected `/admin` dashboard, and an
**email is sent** to the agency when the client submits.

## Pages

| URL        | Who        | What |
|------------|------------|------|
| `/`        | The client | The review page (share this unlisted link) |
| `/admin`   | The agency | Dashboard of live decisions + submissions (needs the admin key) |

## Run locally

```bash
npm install
cp .env.example .env      # edit values
npm start                 # http://localhost:3000
```

## Deploy (public link)

**Render (recommended, free):**
1. Push this repo to GitHub (done).
2. On [render.com](https://render.com): **New → Blueprint**, connect this repo.
   It reads `render.yaml` and creates the web service.
3. In the service's **Environment** tab, set `SMTP_*` (see below) to turn on
   email. Note the generated `ADMIN_KEY` under Environment.
4. Your public URL is `https://<service>.onrender.com`. Share `/` with the
   client; open `/admin` yourself and enter the admin key.

The free plan sleeps after inactivity, so the first visit can take ~30–60s to
wake — normal, not an error. Free storage is ephemeral (see `render.yaml`);
the emailed summary on submit is the durable record.

Any Node host works (Railway, Fly.io, a VPS) — just run `npm start` with the
environment variables below.

## Configuration

| Variable | Purpose |
|----------|---------|
| `NOTIFY_EMAIL` | Address emailed on submission (default `youraistarr@gmail.com`) |
| `ADMIN_KEY` | Password for `/admin` |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` / `SMTP_FROM` | SMTP for notifications. For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833). |
| `DATA_DIR` | Where the JSON store is written (default `./data`; point at a mounted disk for durability) |

If SMTP is not set, submissions are still stored and shown on `/admin`; they
just aren't emailed. The client can also Copy/Download their summary as a
backup from the submit dialog.

## Notes

- Post images use the Google Drive links from the original campaign board; they
  display for anyone who can access those shared files, and degrade to a styled
  navy card (headline still readable) if one can't load.
- "Unlisted" means there's no login on `/` — anyone with the link can review.
  Keep the link private to your client.
