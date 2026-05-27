"""
Islamorada Chamber of Commerce member contact scraper.

Usage:
    1. Export the member Google Sheet as CSV -> save as members.csv in this directory
    2. pip install -r requirements.txt
    3. python3 scraper.py
    4. Import members_updated.csv back into Google Sheets
"""

import csv
import json
import os
import random
import re
import time
import urllib.parse
import urllib3
from collections import defaultdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

COLUMN_KNOWN_VIA = "Known via"
COLUMN_BIZ_NAME = "Business Name"
COLUMN_CONTACT = "Contact Name"
COLUMN_EMAIL = "Email Address"
COLUMN_PHONE = "Phone Number"
COLUMN_WEBSITE = "Website URL"
COLUMN_FACEBOOK = "Facebook Page URL"
COLUMN_CATEGORY = "Business Category"
COLUMN_NOTES = "Notes"

SUBPAGES_TO_TRY = ["/contact", "/contact-us", "/about", "/about-us", "/team", "/staff"]
REQUEST_TIMEOUT = 12
RATE_DELAY_MIN = 1.0
RATE_DELAY_MAX = 2.5
MAX_HTML_SIZE = 2_000_000  # 2 MB cap to avoid huge pages

INPUT_FILE = "members.csv"
OUTPUT_FILE = "members_updated.csv"
CHECKPOINT_FILE = "scrape_checkpoint.json"
LOG_FILE = "scrape_log.txt"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

EMAIL_LOCAL_BLACKLIST = {
    "noreply", "no-reply", "donotreply", "do-not-reply",
    "webmaster", "postmaster", "abuse", "spam",
    "test", "demo", "sentry", "support@sentry", "admin",
    "bounce", "mailer-daemon", "unsubscribe",
}

DOMAIN_BLACKLIST = {
    "example.com", "sentry.io", "wixpress.com", "squarespace.com",
    "amazonaws.com", "cloudflare.com", "schema.org", "w3.org",
    "yourdomain.com", "domain.com", "email.com", "mailchimp.com",
    "mailgun.com", "sendgrid.net", "constantcontact.com",
    "googleapis.com", "google.com", "apple.com", "microsoft.com",
    "gravatar.com", "wordpress.com", "wix.com", "godaddy.com",
    "jquery.com", "bootstrapcdn.com", "fontawesome.com",
}

FB_NOISE_PATHS = {
    "/sharer", "/share", "/plugins", "/tr", "/dialog",
    "/ajax", "/watch", "/groups", "/events", "/hashtag",
    "/photo", "/video", "/stories", "/marketplace",
    "/gaming", "/notifications", "/messages", "/login",
    "/signup", "/search",
}

# Regex compiled once
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

FB_RAW_PATTERN = re.compile(
    r"https?://(?:www\.)?facebook\.com/([A-Za-z0-9_.%-]+)(?:[/?#][^\s\"'<>]*)?"
)

# Suppress SSL warnings for sites with expired certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

_log_file = None


def _get_log():
    global _log_file
    if _log_file is None:
        _log_file = open(LOG_FILE, "a", encoding="utf-8")
    return _log_file


def log_message(message: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {level}: {message}"
    print(line)
    _get_log().write(line + "\n")
    _get_log().flush()


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------

def load_checkpoint() -> dict:
    if not os.path.exists(CHECKPOINT_FILE):
        return {}
    try:
        with open(CHECKPOINT_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_checkpoint(checkpoint: dict) -> None:
    tmp = CHECKPOINT_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2)
    os.replace(tmp, CHECKPOINT_FILE)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def normalize_url(url: str) -> str:
    url = url.strip().rstrip("/").lower()
    if url and not url.startswith("http"):
        url = "https://" + url
    return url


def fetch_html(url: str, session: requests.Session) -> tuple:
    """Returns (html_text, final_url) or (None, url) on error."""
    for verify in (True, False):
        try:
            resp = session.get(
                url,
                timeout=REQUEST_TIMEOUT,
                verify=verify,
                stream=True,
            )
            resp.raise_for_status()
            content = b""
            for chunk in resp.iter_content(chunk_size=32768):
                content += chunk
                if len(content) > MAX_HTML_SIZE:
                    break
            html = content.decode(resp.apparent_encoding or "utf-8", errors="replace")
            return html, str(resp.url)
        except requests.exceptions.SSLError:
            if not verify:
                log_message(f"SSL error (even with verify=False): {url}", "WARN")
                return None, url
            # retry with verify=False
            continue
        except requests.exceptions.Timeout:
            log_message(f"Timeout: {url}", "WARN")
            return None, url
        except requests.exceptions.TooManyRedirects:
            log_message(f"Too many redirects: {url}", "WARN")
            return None, url
        except requests.exceptions.ConnectionError as e:
            log_message(f"Connection error {url}: {e}", "WARN")
            return None, url
        except requests.exceptions.HTTPError as e:
            log_message(f"HTTP error {url}: {e}", "WARN")
            return None, url
        except Exception as e:
            log_message(f"Unexpected error {url}: {e}", "WARN")
            return None, url
    return None, url


def _rate_limit() -> None:
    time.sleep(random.uniform(RATE_DELAY_MIN, RATE_DELAY_MAX))


# ---------------------------------------------------------------------------
# Email extraction
# ---------------------------------------------------------------------------

def extract_emails(html: str, base_domain: str = "") -> list:
    candidates = EMAIL_PATTERN.findall(html)

    # Also grab mailto: hrefs via BeautifulSoup (catches obfuscated ones)
    try:
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().startswith("mailto:"):
                addr = href[7:].split("?")[0].strip()
                if EMAIL_PATTERN.fullmatch(addr):
                    candidates.append(addr)
    except Exception:
        pass

    results = []
    seen = set()
    for email in candidates:
        email = email.strip().lower()
        if email in seen:
            continue
        seen.add(email)

        local, _, domain = email.partition("@")

        # Filter blacklisted local parts
        if any(local.startswith(bl) for bl in EMAIL_LOCAL_BLACKLIST):
            continue

        # Filter blacklisted domains
        if domain in DOMAIN_BLACKLIST:
            continue

        # Filter image/font false positives
        if re.search(r"\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot|ico|css|js)$", domain, re.I):
            continue

        # Filter suspiciously long local parts (usually base64/encoded data)
        if len(local) > 50:
            continue

        # Prefer same-domain emails first (sort later)
        results.append((email, domain == base_domain))

    # Sort: same-domain first
    results.sort(key=lambda x: (not x[1], x[0]))
    return [e for e, _ in results]


# ---------------------------------------------------------------------------
# Facebook extraction
# ---------------------------------------------------------------------------

def normalize_facebook_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    clean = urllib.parse.urlunparse((
        "https",
        "www.facebook.com",
        parsed.path.rstrip("/"),
        "", "", ""
    ))
    return clean


def extract_facebook_urls(html: str) -> list:
    found = []
    seen = set()

    def _consider(href: str):
        if not href or "facebook.com/" not in href.lower():
            return
        try:
            parsed = urllib.parse.urlparse(href)
        except Exception:
            return
        path = parsed.path.rstrip("/")
        if not path or path == "/":
            return
        if any(path.lower().startswith(noise) for noise in FB_NOISE_PATHS):
            return
        # Must look like a page/profile path (no bare domain)
        normalized = normalize_facebook_url(href)
        if normalized not in seen:
            seen.add(normalized)
            found.append(normalized)

    try:
        soup = BeautifulSoup(html, "lxml")

        # <a href> tags
        for a in soup.find_all("a", href=True):
            _consider(a["href"])

        # <meta property="og:..." content="..."> or similar
        for meta in soup.find_all("meta"):
            for attr in ("content", "value"):
                val = meta.get(attr, "")
                if "facebook.com/" in val:
                    _consider(val)

    except Exception:
        pass

    # Raw regex fallback on the full HTML string
    for match in FB_RAW_PATTERN.finditer(html):
        _consider(match.group(0))

    return found


# ---------------------------------------------------------------------------
# Core scraper
# ---------------------------------------------------------------------------

def scrape_website(url: str, session: requests.Session) -> dict:
    result = {"email": None, "facebook": None}

    pages_to_try = [url] + [url + sub for sub in SUBPAGES_TO_TRY]

    base_domain = ""
    try:
        base_domain = urllib.parse.urlparse(url).netloc.lower().lstrip("www.")
    except Exception:
        pass

    homepage_failed = False
    for i, page_url in enumerate(pages_to_try):
        # If the homepage itself hard-failed, skip subpages — same block will apply
        if i > 0 and homepage_failed:
            break

        html, _ = fetch_html(page_url, session)
        _rate_limit()

        if html is None:
            if i == 0:
                homepage_failed = True
            continue

        if result["email"] is None:
            emails = extract_emails(html, base_domain)
            if emails:
                result["email"] = emails[0]

        if result["facebook"] is None:
            fb_urls = extract_facebook_urls(html)
            if fb_urls:
                result["facebook"] = fb_urls[0]

        if result["email"] and result["facebook"]:
            break

    return result


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def load_input_csv(path: str) -> tuple:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Input file '{path}' not found.\n"
            "Please export the Google Sheet as CSV and save it as members.csv"
        )
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return rows, list(fieldnames)


def save_output_csv(rows: list, fieldnames: list, path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Row filtering
# ---------------------------------------------------------------------------

def should_skip_row(row: dict) -> tuple:
    website = row.get(COLUMN_WEBSITE, "").strip()
    if not website:
        return True, "no website"
    email = row.get(COLUMN_EMAIL, "").strip()
    facebook = row.get(COLUMN_FACEBOOK, "").strip()
    if email and facebook:
        return True, "already complete"
    return False, ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Islamorada Chamber Member Contact Scraper")
    print("=" * 60)

    rows, fieldnames = load_input_csv(INPUT_FILE)
    log_message(f"Loaded {len(rows)} rows from {INPUT_FILE}")

    checkpoint = load_checkpoint()
    log_message(f"Checkpoint has {len(checkpoint)} cached URLs")

    session = requests.Session()
    session.headers.update(HEADERS)
    session.max_redirects = 10

    # Build URL -> list of rows index (handles shared websites)
    url_to_rows = defaultdict(list)
    for row in rows:
        raw = row.get(COLUMN_WEBSITE, "").strip()
        if raw:
            url = normalize_url(raw)
            url_to_rows[url].append(row)

    # Determine which URLs actually need scraping
    urls_to_scrape = []
    for url, url_rows in url_to_rows.items():
        if all(should_skip_row(r)[0] for r in url_rows):
            continue
        urls_to_scrape.append(url)

    log_message(f"Unique URLs to scrape: {len(urls_to_scrape)} "
                f"(of {len(url_to_rows)} total unique sites)")

    found_email = 0
    found_fb = 0

    with tqdm(urls_to_scrape, desc="Scraping", unit="site") as pbar:
        for url in pbar:
            biz_names = [r.get(COLUMN_BIZ_NAME, url) for r in url_to_rows[url]]
            pbar.set_postfix_str(biz_names[0][:35])

            if url in checkpoint:
                result = checkpoint[url]
            else:
                result = scrape_website(url, session)
                checkpoint[url] = result
                save_checkpoint(checkpoint)

            url_rows = url_to_rows[url]
            for row in url_rows:
                skip, _ = should_skip_row(row)
                if skip:
                    continue
                if result.get("email") and not row.get(COLUMN_EMAIL, "").strip():
                    row[COLUMN_EMAIL] = result["email"]
                    found_email += 1
                if result.get("facebook") and not row.get(COLUMN_FACEBOOK, "").strip():
                    row[COLUMN_FACEBOOK] = result["facebook"]
                    found_fb += 1

    save_output_csv(rows, fieldnames, OUTPUT_FILE)

    total = len(rows)
    total_with_email = sum(1 for r in rows if r.get(COLUMN_EMAIL, "").strip())
    total_with_fb = sum(1 for r in rows if r.get(COLUMN_FACEBOOK, "").strip())

    print("\n" + "=" * 60)
    print("Done!")
    print(f"  Emails found this run:   {found_email}")
    print(f"  Facebook found this run: {found_fb}")
    print(f"  Rows with email now:     {total_with_email}/{total}")
    print(f"  Rows with Facebook now:  {total_with_fb}/{total}")
    print(f"  Output written to:       {OUTPUT_FILE}")
    print("=" * 60)

    _get_log().close()


if __name__ == "__main__":
    main()
