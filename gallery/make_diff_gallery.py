"""Generate diff_gallery.html by comparing slides.json on any branch to a base branch."""

import argparse
import json
import subprocess


SLIDES_PATH = "../json/slides.json"
DEFAULT_BASE = "main"
SLIDES_PATH_FROM_REPO_ROOT = "json/slides.json"
OUTPUT = "diff_gallery.html"


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def load_slides_from_ref(ref):
    raw = git("show", f"{ref}:{SLIDES_PATH_FROM_REPO_ROOT}")
    return json.loads(raw)


def load_branch_slides(branch=None):
    if branch is not None:
        return load_slides_from_ref(branch)
    with open(SLIDES_PATH) as f:
        return json.load(f)


def diff_slides(main_slides, branch_slides):
    """Pair slides between main and branch.

    Some slides share a link (e.g. /congress/senate appears with multiple
    titles), so we can't key purely on link. Strategy: first claim exact
    content matches (unchanged), then pair the rest by (link, title) to
    detect modifications. Whatever's left is added or removed.
    """
    main_remaining = list(main_slides)
    branch_remaining = list(branch_slides)
    unchanged = []

    for slide in list(branch_remaining):
        if slide in main_remaining:
            unchanged.append(slide)
            main_remaining.remove(slide)
            branch_remaining.remove(slide)

    def mod_key(s):
        return (s.get("link"), s.get("title"))

    modified = []
    for branch_slide in list(branch_remaining):
        target = mod_key(branch_slide)
        main_match = next((m for m in main_remaining if mod_key(m) == target), None)
        if main_match is not None:
            modified.append({"main": main_match, "branch": branch_slide})
            main_remaining.remove(main_match)
            branch_remaining.remove(branch_slide)

    return branch_remaining, main_remaining, modified, unchanged


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Slide Diff Gallery</title>
<style>
:root {
    --added-bg: #e8f7ee;
    --added-border: #28a745;
    --removed-bg: #fbeaea;
    --removed-border: #dc3545;
    --modified-bg: #fff8e1;
    --modified-border: #f5a623;
    --neutral-border: #d0d0d0;
}
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin: 0;
    padding: 24px;
    background: #fafafa;
    color: #222;
}
h1 { margin: 0 0 4px; font-size: 22px; }
.subtitle { color: #666; margin-bottom: 18px; font-size: 14px; }
.summary {
    display: flex;
    gap: 16px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}
.pill {
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid;
    background: white;
}
.pill.added { color: var(--added-border); border-color: var(--added-border); }
.pill.removed { color: var(--removed-border); border-color: var(--removed-border); }
.pill.modified { color: var(--modified-border); border-color: var(--modified-border); }
.pill.unchanged { color: #666; border-color: #ccc; }
.section { margin-bottom: 36px; }
.section h2 {
    font-size: 16px;
    margin: 0 0 12px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #555;
}
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 16px;
}
.card {
    background: white;
    border: 2px solid var(--neutral-border);
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.card.added { border-color: var(--added-border); background: var(--added-bg); }
.card.removed { border-color: var(--removed-border); background: var(--removed-bg); }
.card.modified { border-color: var(--modified-border); background: var(--modified-bg); }
.media {
    width: 100%;
    aspect-ratio: 16 / 5;
    background: #333 center/cover no-repeat;
    border-bottom: 1px solid rgba(0,0,0,.06);
    position: relative;
}
.media.missing::after {
    content: "image not found";
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ddd;
    font-size: 12px;
    font-style: italic;
}
.mask-light::after { background: rgba(255,255,255,0.25); }
.mask-medium::after { background: rgba(0,0,0,0.35); }
.mask-strong::after { background: rgba(0,0,0,0.55); }
.body { padding: 12px 14px; }
.title { font-weight: 600; font-size: 15px; margin: 0 0 6px; }
.caption { font-size: 13px; color: #444; line-height: 1.4; margin: 0 0 10px; }
.meta {
    font-size: 11px;
    color: #777;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.meta a { color: #1565c0; text-decoration: none; }
.meta a:hover { text-decoration: underline; }
.modified .pair {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border-top: 1px dashed #ddd;
}
.pair > div { padding: 12px 14px; }
.pair > div + div { border-left: 1px dashed #ddd; }
.pair-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin-bottom: 6px;
}
details.unchanged-block summary {
    cursor: pointer;
    color: #666;
    font-size: 14px;
}
details.unchanged-block .cards { margin-top: 12px; }
.empty {
    color: #888;
    font-style: italic;
    padding: 8px 0;
}
</style>
</head>
<body>
<h1>Slide Diff Gallery</h1>
<div class="subtitle">
    branch <strong id="branchName"></strong> compared to <strong id="baseName"></strong>
    &middot; <span id="mainCount"></span> on main, <span id="branchCount"></span> on branch
</div>

<div class="summary">
    <span class="pill added"><span id="addedCount"></span> added</span>
    <span class="pill removed"><span id="removedCount"></span> removed</span>
    <span class="pill modified"><span id="modifiedCount"></span> modified</span>
    <span class="pill unchanged"><span id="unchangedCount"></span> unchanged</span>
</div>

<div class="section">
    <h2>Added (only on branch)</h2>
    <div id="addedCards" class="cards"></div>
</div>

<div class="section">
    <h2>Removed (only on main)</h2>
    <div id="removedCards" class="cards"></div>
</div>

<div class="section">
    <h2>Modified (different between branch and main)</h2>
    <div id="modifiedCards" class="cards"></div>
</div>

<details class="unchanged-block section">
    <summary>Unchanged (<span id="unchangedSummaryCount"></span>) — click to expand</summary>
    <div id="unchangedCards" class="cards"></div>
</details>

<script>
const DATA = __DATA__;

const VOTEVIEW_BASE = 'https://voteview.com';
const IMG_BASE = '../images/';

document.getElementById('branchName').textContent = DATA.branch_name;
document.getElementById('baseName').textContent = DATA.base_name;
document.getElementById('mainCount').textContent = DATA.main_count;
document.getElementById('branchCount').textContent = DATA.branch_count;
document.getElementById('addedCount').textContent = DATA.added.length;
document.getElementById('removedCount').textContent = DATA.removed.length;
document.getElementById('modifiedCount').textContent = DATA.modified.length;
document.getElementById('unchangedCount').textContent = DATA.unchanged.length;
document.getElementById('unchangedSummaryCount').textContent = DATA.unchanged.length;

function escapeHtml(s) {
    return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function mediaHtml(slide) {
    const media = slide.image || slide.video || '';
    if (slide.video) {
        return `<div class="media" style="background:#222 center/contain no-repeat;">
                  <video src="${escapeHtml(IMG_BASE + slide.video)}" muted style="width:100%;height:100%;object-fit:cover;"></video>
                </div>`;
    }
    if (media) {
        return `<div class="media" style="background-image:url('${escapeHtml(IMG_BASE + media)}');"></div>`;
    }
    return `<div class="media missing"></div>`;
}

function metaHtml(slide) {
    const parts = [];
    if (slide.link) {
        parts.push(`<a href="${escapeHtml(VOTEVIEW_BASE + slide.link)}" target="_blank" rel="noopener">${escapeHtml(slide.link)}</a>`);
    }
    if (slide.weight != null) parts.push(`weight: ${escapeHtml(slide.weight)}`);
    if (slide.mask) parts.push(`mask: ${escapeHtml(slide.mask)}`);
    return `<div class="meta">${parts.join('')}</div>`;
}

function cardHtml(slide, cls) {
    return `<div class="card ${cls}">
        ${mediaHtml(slide)}
        <div class="body">
            <p class="title">${escapeHtml(slide.title || '(no title)')}</p>
            <p class="caption">${escapeHtml(slide.caption || '')}</p>
            ${metaHtml(slide)}
        </div>
    </div>`;
}

function modifiedCardHtml(pair) {
    const a = pair.main, b = pair.branch;
    return `<div class="card modified">
        ${mediaHtml(b)}
        <div class="body">
            <p class="title">${escapeHtml(b.title || '(no title)')}</p>
        </div>
        <div class="pair">
            <div>
                <div class="pair-label">main</div>
                <p class="caption">${escapeHtml(a.caption || '')}</p>
                ${metaHtml(a)}
            </div>
            <div>
                <div class="pair-label">branch</div>
                <p class="caption">${escapeHtml(b.caption || '')}</p>
                ${metaHtml(b)}
            </div>
        </div>
    </div>`;
}

function render(targetId, items, builder, emptyMsg) {
    const t = document.getElementById(targetId);
    if (!items.length) {
        t.innerHTML = `<div class="empty">${emptyMsg}</div>`;
        return;
    }
    t.innerHTML = items.map(builder).join('');
}

render('addedCards', DATA.added, s => cardHtml(s, 'added'), 'No additions on this branch.');
render('removedCards', DATA.removed, s => cardHtml(s, 'removed'), 'No removals on this branch.');
render('modifiedCards', DATA.modified, modifiedCardHtml, 'No modified slides.');
render('unchangedCards', DATA.unchanged, s => cardHtml(s, 'unchanged'), 'None.');
</script>
</body>
</html>
"""


def build(branch=None, base=DEFAULT_BASE):
    branch_name = branch if branch is not None else git("rev-parse", "--abbrev-ref", "HEAD")
    base_slides = load_slides_from_ref(base)
    branch_slides = load_branch_slides(branch)
    added, removed, modified, unchanged = diff_slides(base_slides, branch_slides)

    data = {
        "branch_name": branch_name,
        "base_name": base,
        "main_count": len(base_slides),
        "branch_count": len(branch_slides),
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
    }

    data_json = json.dumps(data, indent=2)
    html = HTML_TEMPLATE.replace("__DATA__", data_json)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(
        f"Wrote {OUTPUT}: branch={branch_name} base={base} "
        f"added={len(added)} removed={len(removed)} "
        f"modified={len(modified)} unchanged={len(unchanged)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate diff_gallery.html comparing a branch to a base branch."
    )
    parser.add_argument(
        "--branch", "-b",
        metavar="BRANCH",
        default=None,
        help="Branch (or ref) to compare (default: current working tree)",
    )
    parser.add_argument(
        "--base",
        metavar="BASE",
        default=DEFAULT_BASE,
        help=f"Base branch to compare against (default: {DEFAULT_BASE})",
    )
    args = parser.parse_args()
    build(branch=args.branch, base=args.base)
