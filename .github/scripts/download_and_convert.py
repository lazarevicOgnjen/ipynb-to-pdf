#!/usr/bin/env python3
"""
Download every .ipynb attached / linked in the issue body
and convert it to PDF inside uploads/
"""

import os
import re
import sys
import json
import requests

EVENT_PATH = os.environ["GITHUB_EVENT_PATH"]
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def main():
    with open(EVENT_PATH, "r", encoding="utf-8") as f:
        event = json.load(f)

    body = event["issue"]["body"] or ""

    # 1. GitHub-issue attachment URLs  (user uploaded file)
    att_urls = re.findall(
        r"https://github\.com/[^/\s]+/[^/\s]+/files/\d+/[^\s)]+\.ipynb[^)\s]*",
        body,
        flags=re.IGNORECASE,
    )

    # 2. Fallback: raw GitHub URLs
    if not att_urls:
        att_urls = re.findall(
            r"https://raw\.githubusercontent\.com/[^\s)]+\.ipynb[^)\s]*",
            body,
            flags=re.IGNORECASE,
        )

    if not att_urls:
        print("❌  No .ipynb file found in issue body.")
        sys.exit(1)

    for url in att_urls:
        url = url.split("?")[0]  # remove query string
        name = os.path.basename(url)
        if not name.lower().endswith(".ipynb"):
            continue
        nb_path = os.path.join(UPLOAD_DIR, name)
        print(f"⬇️  Downloading {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(nb_path, "wb") as f:
            f.write(r.content)

        pdf_name = name[:-6] + ".pdf"
        print(f"🔄  Converting  ->  {pdf_name}")
        os.system(
            f'jupyter nbconvert "{nb_path}" --to pdf --output-dir="{UPLOAD_DIR}"'
        )


if __name__ == "__main__":
    main()
