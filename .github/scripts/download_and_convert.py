#!/usr/bin/env python3
import os, re, sys, json, requests, subprocess
from pathlib import Path

EVENT_PATH   = os.environ["GITHUB_EVENT_PATH"]
UPLOAD_DIR   = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def main():
    with open(EVENT_PATH, "r", encoding="utf-8") as f:
        event = json.load(f)

    body = event["issue"]["body"] or ""

    # 1. markdown  [text](url)
    md_links = re.findall(r'\[([^\]]+)\]\((https://github\.com/[^\s)]+\.ipynb[^)\s]*)\)', body, flags=re.I)
    urls = [url for _, url in md_links]

    # 2. raw githubusercontent
    urls += re.findall(r'(https://raw\.githubusercontent\.com/[^\s)]+\.ipynb[^)\s]*)', body, flags=re.I)

    # 3. direktni github attachment
    urls += re.findall(r'(https://github\.com/[^/\s]+/[^/\s]+/files/\d+/[^\s)]+\.ipynb[^)\s]*)', body, flags=re.I)

    if not urls:
        print("❌  No .ipynb file found in issue body.")
        sys.exit(1)

    for url in urls:
        url = url.split("?")[0]
        name = Path(url).name
        nb_path = UPLOAD_DIR / name
        print(f"⬇️  Downloading {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        nb_path.write_bytes(r.content)

        pdf_name = nb_path.with_suffix(".pdf").name
        print(f"🔄  Converting  ->  {pdf_name}")
        cmd = f'jupyter nbconvert "{nb_path}" --to pdf --output-dir="{UPLOAD_DIR}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("nbconvert ERROR:", result.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
