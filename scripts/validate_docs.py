#!/usr/bin/env python3
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ALLOWED_RELS = {
    "related",
    "companion",
    "responds_to",
    "implications_for",
    "informed_by",
    "supersedes",
    "superseded_by",
    "implements",
    "depends_on",
    "blocks",
    "references",
    "contradicts",
    "duplicates",
}

REQUIRED_LLM_SECTIONS = [
    "LLM Summary",
    "Canonical Statements",
    "Scope and Non-Goals",
    "Dependencies and Interfaces",
    "Evidence and Freshness",
    "Open Questions",
    "Change Log",
]

CORE_PREFIXES = ("SYS-", "DD-", "STD-", "ADR-")
CORE_IDS = {"IDX-00-MASTER"}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        return None
    block = m.group(1)
    lines = block.splitlines()
    data = {}
    i = 0
    key_re = re.compile(r"^[A-Za-z0-9_-]+:")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if key_re.match(line):
            key, rest = line.split(":", 1)
            key = key.strip()
            val = rest.strip()
            if key == "links":
                if val == "[]":
                    data["links"] = []
                    i += 1
                    continue
                if val:
                    data["links"] = "__invalid__"
                    i += 1
                    continue
                i += 1
                links = []
                current = None
                while i < len(lines) and (lines[i].startswith("  -") or lines[i].startswith("    ")):
                    l = lines[i]
                    if l.startswith("  - "):
                        if current:
                            links.append(current)
                        current = {}
                        rest = l[4:]
                        if ":" in rest:
                            k, v = rest.split(":", 1)
                            current[k.strip()] = v.strip().strip('"').strip("'")
                    elif l.startswith("    ") and ":" in l:
                        k, v = l.strip().split(":", 1)
                        if current is None:
                            current = {}
                        current[k.strip()] = v.strip().strip('"').strip("'")
                    i += 1
                if current:
                    links.append(current)
                data["links"] = links
                continue

            if val == "":
                items = []
                i += 1
                while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                    item = re.sub(r"^\s*-\s+", "", lines[i]).strip()
                    item = item.strip('"').strip("'")
                    items.append(item)
                    i += 1
                data[key] = items
                continue
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if inner:
                    items = [v.strip().strip('"').strip("'") for v in inner.split(",")]
                else:
                    items = []
                data[key] = items
            elif val == "[]":
                data[key] = []
            elif val.lower() == "null":
                data[key] = None
            else:
                data[key] = val.strip('"').strip("'")
        i += 1
    return data


def is_core_id(doc_id):
    if not doc_id:
        return False
    if doc_id in CORE_IDS:
        return True
    return doc_id.startswith(CORE_PREFIXES)


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None


def extract_llm_summary(text):
    m = re.search(r"## LLM Summary\n(.*?)(\n## |\Z)", text, flags=re.S)
    if not m:
        return None
    return m.group(1).strip()


def check_required_sections(text):
    missing = []
    for section in REQUIRED_LLM_SECTIONS:
        if f"## {section}" not in text:
            missing.append(section)
    return missing


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9]+", text or ""))


def main():
    parser = argparse.ArgumentParser(description="Validate Compass docs and LLM views")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if errors are found")
    args = parser.parse_args()

    root = Path(".")
    canonical_files = [
        p
        for p in root.glob("*.md")
        if p.name.startswith(("ADR-", "RF-", "DD-", "STD-", "SYS-", "IDX-"))
    ]

    canonical = {}
    canonical_ids = set()
    for p in canonical_files:
        data = parse_frontmatter(p.read_text())
        if not data:
            continue
        doc_id = data.get("id")
        if not doc_id:
            continue
        canonical[doc_id] = {"path": p, "data": data}
        canonical_ids.add(doc_id)

    llm_views = {}
    for p in Path("llm").glob("LLM-*.md"):
        data = parse_frontmatter(p.read_text())
        if not data:
            continue
        source_id = data.get("source_id")
        if source_id:
            llm_views[source_id] = {"path": p, "data": data}

    errors = []
    warnings = []

    # Check LLM views exist for each canonical doc
    for doc_id, info in sorted(canonical.items()):
        if doc_id not in llm_views:
            errors.append(f"Missing LLM view for {doc_id} ({info['path'].name})")

    # Validate canonical links
    for doc_id, info in sorted(canonical.items()):
        data = info["data"]
        links = data.get("links")
        if links is None:
            if is_core_id(doc_id):
                warnings.append(f"Missing links for core doc {doc_id} ({info['path'].name})")
            continue
        if links == "__invalid__" or not isinstance(links, list):
            errors.append(f"Invalid links format in {doc_id} ({info['path'].name})")
            continue
        for idx, link in enumerate(links):
            if not isinstance(link, dict):
                errors.append(f"Invalid links entry in {doc_id} ({info['path'].name})")
                continue
            rel = link.get("rel")
            target_id = link.get("target_id")
            if not rel or not target_id:
                errors.append(f"Links entry missing rel/target_id in {doc_id} ({info['path'].name})")
                continue
            if rel not in ALLOWED_RELS:
                errors.append(f"Invalid rel '{rel}' in {doc_id} ({info['path'].name})")
            if target_id not in canonical_ids:
                errors.append(f"Unknown target_id '{target_id}' in {doc_id} ({info['path'].name})")

    # Validate LLM views
    for source_id, info in sorted(llm_views.items()):
        path = info["path"]
        data = info["data"]
        text = path.read_text()

        canonical_info = canonical.get(source_id)
        if not canonical_info:
            errors.append(f"LLM view has unknown source_id {source_id} ({path.name})")
            continue

        source_updated = data.get("source_updated")
        canonical_updated = canonical_info["data"].get("updated")
        if source_updated and canonical_updated and source_updated != canonical_updated:
            warnings.append(
                f"Stale LLM view for {source_id}: source_updated {source_updated} != canonical updated {canonical_updated}"
            )
            staleness = data.get("staleness")
            d1 = parse_date(source_updated)
            d2 = parse_date(canonical_updated)
            if d1 and d2:
                delta_days = (d2 - d1).days
                if delta_days <= 0:
                    expected = "fresh"
                elif delta_days <= 30:
                    expected = "review"
                else:
                    expected = "stale"
                if staleness and staleness != expected:
                    warnings.append(
                        f"Staleness mismatch for {source_id}: expected {expected}, found {staleness}"
                    )
        elif not source_updated or not canonical_updated:
            warnings.append(f"Missing source_updated or canonical updated for {source_id} ({path.name})")

        summary = extract_llm_summary(text)
        if not summary:
            errors.append(f"Missing LLM Summary in {path.name}")
        else:
            wc = word_count(summary)
            if wc < 120 or wc > 180:
                errors.append(f"LLM Summary out of range in {path.name} ({wc} words)")

        missing_sections = check_required_sections(text)
        if missing_sections:
            errors.append(f"Missing sections in {path.name}: {', '.join(missing_sections)}")

    # Output
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN: {w}")
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
