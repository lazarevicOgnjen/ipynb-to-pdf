#!/usr/bin/env python3
import os, re, requests, json

EVENT_PATH = os.environ["GITHUB_EVENT_PATH"]
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def main():
    with open(EVENT_PATH, "r", encoding="utf-8") as f:
        event = json.load(f)

    body = event["issue"]["body"] or ""

    # 1. Markdown linkovi  [ime](url)
    md_links = re.findall(r'\[([^\]]+)\]\((https://github\.com/[^\s)]+\.ipynb[^)\s]*)\)', body, flags=re.I)
    urls = [url for _, url in md_links]

    # 2. Raw githubusercontent
    raw_links = re.findall(r'(https://raw\.githubusercontent\.com/[^\s)]+\.ipynb[^)\s]*)', body, flags=re.I)
    urls += raw_links

    # 3. Direktni github attachment (bez markdowna)
    bare = re.findall(r'(https://github\.com/[^/\s]+/[^/\s]+/files/\d+/[^\s)]+\.ipynb[^)\s]*)', body, flags=re.I)
    urls += bare

    if not urls:
        print("❌  No .ipynb file found in issue body.")
        exit(1)

    for url in urls:
        url = url.split("?")[0]
        name = os.path.basename(url)
        nb_path = os.path.join(UPLOAD_DIR, name)
        print(f"⬇️  Downloading {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(nb_path, "wb") as f:
            f.write(r.content)

        print(f"🔄  Converting  ->  {name[:-6]}.pdf")
        os.system(f'jupyter nbconvert "{nb_path}" --to pdf --output-dir="{UPLOAD_DIR}"')

if __name__ == "__main__":
    main()
