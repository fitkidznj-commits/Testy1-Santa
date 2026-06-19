# Ari's Landscaping & Paving — Website

A self-contained, responsive, conversion-focused website for **Ari's Landscaping &
Paving** (Islamorada & the Upper Keys), built by a.i. STaRR. No build step, no
dependencies — pure HTML/CSS/JS, ready to deploy anywhere.

Grounded in [`../website-mockup.md`](../website-mockup.md) and
[`../proposal.md`](../proposal.md), with **paving added as a co-equal service**.

## Structure
```
website/
├── index.html                 # Home (hero, services, before/after, reviews, area, about, estimate form)
├── services/
│   ├── landscaping.html        # SEO service page: lawns, design, trimming, sod, cleanups
│   └── paving.html             # SEO service page: driveways, patios, walkways, coral rock, sealing
├── css/styles.css              # Design system (palm green + leaf + sand + paving stone)
├── js/main.js                  # Mobile nav, before/after slider, form handler, year
└── assets/logo.svg             # Placeholder logo
```

## Run locally
Just open `index.html` in a browser, or serve the folder:
```bash
cd 06-ari-landscaping/website
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Deploy (GitHub Pages)
Point Pages at this folder (or copy its contents to the site root). Because there's no
build step, the files serve as-is.

## Features
- Mobile-first, responsive (375px → desktop), accessible (semantic, focus styles, reduced-motion)
- Sticky header + **sticky mobile call/text/estimate bar**
- Persistent "Free Estimate" CTAs (the conversion goal)
- Draggable **before/after slider** (placeholder gradients — swap in real photos)
- FAQ accordions with FAQ-friendly markup, LocalBusiness JSON-LD schema on the home page
- Short lead form with success state

## ⚠️ Client to provide / confirm (placeholders in the markup)
Search the files for `[` brackets and `client to provide/confirm` notes:
- **Logo** (replace `assets/logo.svg`)
- **Phone & email** (all `tel:+10000000000`, `[Phone]`, `[Email]`)
- **License #**, **years in business**, **hours**
- **Exact service area** (currently Islamorada/Tavernier/Key Largo/Plantation Key/Marathon)
- **Real reviews** (replace `[Name]` placeholder testimonials with live Google reviews)
- **Before/after & team photos** (replace gradient/emoji placeholders)
- **Google Map embed** for the service-area block

## Wiring the lead form (production)
The form in `index.html` (`#estimate-form`) currently shows a front-end success message.
In production, POST submissions to the lead-capture endpoint / **Make.com webhook** and
trigger the instant SMS + email auto-reply described in
[`../proposal.md`](../proposal.md) §10. See the marked spot in `js/main.js`.
