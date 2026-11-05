"""Download a revision-pinned copy of Zama's public HF demo; never execute it."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen

SPACE = "zama-fhe/encrypted_sentiment_analysis"
ROOT = Path(__file__).resolve().parent
DEST = ROOT / "upstream"
ALLOWED_ROOTS = {
    "README.md", "app.py", "server.py", "transformer_vectorizer.py",
    "compile.py", "requirements.txt", "SentimentClassification.ipynb",
    "download_data.sh", "sentiment_analysis_banner.png",
    "LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "NOTICE.md",
}


def allowed(name):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        return False
    return name in ALLOWED_ROOTS or (
        p.parts[0] == "deployment"
        and not any(part.startswith(".") for part in p.parts)
        and not any("private" in part.lower() or "secret" in part.lower()
                    for part in p.parts)
    )


def fetch(url):
    request = Request(url, headers={"User-Agent": "zama-demo-source-import/1.0"})
    with urlopen(request, timeout=180) as response:
        return response.read()


def main():
    # Resolve main once; every file below is fetched from the same exact revision.
    info = json.loads(fetch(f"https://huggingface.co/api/spaces/{SPACE}"))
    revision = info["sha"]
    names = sorted(item["rfilename"] for item in info["siblings"]
                   if allowed(item["rfilename"]))
    required = {"app.py", "server.py", "transformer_vectorizer.py", "requirements.txt"}
    if not required.issubset(names) or not any(n.startswith("deployment/") for n in names):
        raise RuntimeError("Upstream layout changed: source/model files missing")
    if DEST.exists():
        raise RuntimeError("upstream/ already exists; refusing to overwrite a published snapshot")
    staging = ROOT / "source-import-staging"
    staging.mkdir(exist_ok=False)
    records = []
    for name in names:
        data = fetch(f"https://huggingface.co/spaces/{SPACE}/resolve/{revision}/{quote(name, safe='/')}")
        if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise RuntimeError(f"Unresolved Git LFS pointer: {name}")
        target = staging / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    # Avoid republishing inherited notebook cell outputs or execution counters.
    for notebook in staging.rglob("*.ipynb"):
        nb = json.loads(notebook.read_text())
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
        notebook.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    os.rename(staging, DEST)
    (ROOT / "SOURCE_MANIFEST.json").write_text(json.dumps({
        "source": f"https://huggingface.co/spaces/{SPACE}",
        "revision": revision,
        "excluded": [".fhe_keys/", "tmp/", "Git metadata", "notebook outputs"],
        "hash_note": "SHA-256 values describe downloaded originals before notebook output removal",
        "files": records,
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"Imported {len(records)} files from {SPACE}@{revision}")


if __name__ == "__main__":
    main()
