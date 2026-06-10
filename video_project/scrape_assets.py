#!/usr/bin/env python3
"""Scrape takedowncharters.com for fishing images and videos."""

import os
import re
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

DEST = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(DEST, exist_ok=True)

PAGES = [
    "https://takedowncharters.com",
    "https://takedowncharters.com/gallery",
    "https://takedowncharters.com/photos",
    "https://takedowncharters.com/media",
    "https://takedowncharters.com/fishing",
    "https://takedowncharters.com/about",
]

SKIP_PATTERNS = re.compile(
    r"(logo|icon|favicon|sprite|pixel|1x1|tracking|analytics|\.svg$|"
    r"placeholder|spinner|loading|thumbnail-placeholder)",
    re.IGNORECASE,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

session = requests.Session()
session.headers.update(HEADERS)

collected_urls = set()


def is_good_url(url):
    if not url:
        return False
    low = url.lower()
    if SKIP_PATTERNS.search(low):
        return False
    if not any(low.endswith(ext) for ext in (
        ".jpg", ".jpeg", ".png", ".webp", ".gif",
        ".mp4", ".mov", ".webm", ".m4v",
    )):
        # allow URLs with query strings that might be images
        if "?" in low:
            base = low.split("?")[0]
            if not any(base.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
                return False
        else:
            return False
    return True


def abs_url(base, href):
    if not href:
        return None
    href = href.strip()
    if href.startswith("data:"):
        return None
    return urllib.parse.urljoin(base, href)


def collect_from_page(page_url):
    try:
        resp = session.get(page_url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [skip] {page_url}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    found = 0

    # <img src / data-src / srcset>
    for img in soup.find_all("img"):
        for attr in ("src", "data-src", "data-lazy-src", "data-original"):
            u = abs_url(page_url, img.get(attr))
            if is_good_url(u) and u not in collected_urls:
                collected_urls.add(u)
                found += 1
        # srcset
        srcset = img.get("srcset", "")
        for part in srcset.split(","):
            u = abs_url(page_url, part.strip().split()[0])
            if is_good_url(u) and u not in collected_urls:
                collected_urls.add(u)
                found += 1

    # <video> and <source>
    for tag in soup.find_all(["video", "source"]):
        for attr in ("src", "data-src"):
            u = abs_url(page_url, tag.get(attr))
            if is_good_url(u) and u not in collected_urls:
                collected_urls.add(u)
                found += 1
        u = abs_url(page_url, tag.get("poster"))
        if is_good_url(u) and u not in collected_urls:
            collected_urls.add(u)
            found += 1

    # OG / twitter meta images
    for meta in soup.find_all("meta"):
        prop = meta.get("property", "") + meta.get("name", "")
        if "image" in prop.lower():
            u = abs_url(page_url, meta.get("content"))
            if is_good_url(u) and u not in collected_urls:
                collected_urls.add(u)
                found += 1

    # inline background-image CSS
    for tag in soup.find_all(style=True):
        matches = re.findall(r'url\(["\']?(.*?)["\']?\)', tag["style"])
        for m in matches:
            u = abs_url(page_url, m)
            if is_good_url(u) and u not in collected_urls:
                collected_urls.add(u)
                found += 1

    # <a href> pointing directly to images/videos
    for a in soup.find_all("a", href=True):
        u = abs_url(page_url, a["href"])
        if is_good_url(u) and u not in collected_urls:
            collected_urls.add(u)
            found += 1

    print(f"  {page_url}: +{found} new URLs (total {len(collected_urls)})")


def download_all():
    downloaded = []
    for i, url in enumerate(sorted(collected_urls), 1):
        ext = url.lower().split("?")[0].rsplit(".", 1)[-1]
        if ext not in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "mov", "webm", "m4v"):
            ext = "jpg"
        fname = f"asset_{i:03d}.{ext}"
        fpath = os.path.join(DEST, fname)
        try:
            r = session.get(url, timeout=20, stream=True)
            r.raise_for_status()
            content_len = int(r.headers.get("content-length", 0))
            if content_len and content_len < 20_000:
                print(f"  [tiny {content_len}B, skip] {url}")
                continue
            with open(fpath, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(fpath)
            if size < 20_000:
                os.remove(fpath)
                print(f"  [tiny {size}B after download, skip] {url}")
                continue
            downloaded.append((fpath, size, url))
            print(f"  [{i:03d}] {fname}  {size//1024}KB  {url}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [fail] {url}: {e}")
    return downloaded


if __name__ == "__main__":
    print("=== Scraping pages ===")
    for page in PAGES:
        collect_from_page(page)

    print(f"\n=== Downloading {len(collected_urls)} assets ===")
    downloaded = download_all()

    print(f"\n=== Done: {len(downloaded)} files in {DEST} ===")
    for fpath, size, url in sorted(downloaded, key=lambda x: -x[1])[:30]:
        print(f"  {os.path.basename(fpath)}  {size//1024}KB")
