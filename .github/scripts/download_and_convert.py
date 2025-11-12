import os
import re
import requests
import json

event_path = os.environ["GITHUB_EVENT_PATH"]
with open(event_path) as f:
    event = json.load(f)

body = event["issue"]["body"]
os.makedirs("uploads", exist_ok=True)

# pronađi markdown linkove ili raw github linkove
urls = re.findall(r'(https://github\.com[^\s\)]+\.ipynb[^>\s]*)', body)

if not urls:
    print("Nema .ipynb fajla u issue-u.")
    exit(1)

for url in urls:
    # pretvori u raw url ako nije
    raw = url.replace("github.com", "raw.githubusercontent.com").replace("/blob", "")
    name = os.path.basename(raw).split("?")[0]
    r = requests.get(raw)
    r.raise_for_status()
    nb_path = f"uploads/{name}"
    with open(nb_path, "wb") as f:
        f.write(r.content)
    # konvertuj
    os.system(f"jupyter nbconvert '{nb_path}' --to pdf --output-dir uploads")
