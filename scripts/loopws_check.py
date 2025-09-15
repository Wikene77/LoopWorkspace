import os, json, re
from urllib.request import Request, urlopen

API_RELEASE = "https://api.github.com/repos/LoopKit/LoopWorkspace/releases/latest"
API_TAGS    = "https://api.github.com/repos/LoopKit/LoopWorkspace/tags"
STATE_FILE  = ".loopws_last.json"

def fetch(url, token=None):
    headers = {"User-Agent": "LoopNewsBot/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def load_state():
    return json.load(open(STATE_FILE, "r", encoding="utf-8")) if os.path.exists(STATE_FILE) else {}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w", encoding="utf-8"))

def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    # Prøv release først
    try:
        rel = json.loads(fetch(API_RELEASE, token))
        tag = rel.get("tag_name") or rel.get("name")
        url = rel.get("html_url")
        src = "release"
    except Exception:
        rel = {}
        tag = None
        url = None
        src = None

    # Fallback: første tag
    if not tag:
        tags = json.loads(fetch(API_TAGS, token))
        if isinstance(tags, list) and tags:
            tag = tags[0].get("name")
            url = f"https://github.com/LoopKit/LoopWorkspace/tree/{tag}"
            src = "tag"

    if not tag:
        print("::notice title=LoopWorkspace::Fant ingen release/tag.")
        return

    state = load_state()
    if state.get("last_tag") == tag:
        print("::notice title=LoopWorkspace::Ingen endring.")
        return

    msg = f"**LoopWorkspace – ny {src}: {tag}**\n{url}"
    print(msg)
    state["last_tag"] = tag
    save_state(state)

if __name__ == "__main__":
    main()
