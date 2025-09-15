import os, re, json
from urllib.request import Request, urlopen

URL = "https://www.loopandlearn.org/version-updates/"
STATE_FILE = ".lnl_last.json"

def fetch(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def extract_latest(html):
    m = re.search(r"(Loop\s+\d+\.\d+(?:\.\d+)?)\s+was released on\s+([A-Za-z0-9 ,.-]+)", html, re.I)
    if m:
        return f"{m.group(1).strip()} | {m.group(2).strip()}"
    m2 = re.search(r"(Loop\s+\d+\.\d+(?:\.\d+)?)", html)
    return m2.group(1).strip() if m2 else None

def load_state():
    return json.load(open(STATE_FILE,"r",encoding="utf-8")) if os.path.exists(STATE_FILE) else {}

def save_state(state):
    json.dump(state, open(STATE_FILE,"w",encoding="utf-8"))

def main():
    html = fetch(URL)
    latest = extract_latest(html)
    if not latest:
        print("::notice title=LnL::Ingen versjon funnet.")
        return
    state = load_state()
    if state.get("latest") == latest:
        print("::notice title=LnL::Ingen endring.")
        return
    print(f"**Loop and Learn – nye versjonsnotater:** {latest}\n{URL}")
    state["latest"] = latest
    save_state(state)

if __name__ == "__main__":
    main()
