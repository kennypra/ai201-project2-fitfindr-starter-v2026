"""
Mark each try in a run_eval.py report PASS or FAIL, using criteria.md as written.

    python check_run.py results/run_<stamp>_before.md

This only counts. Whether a criterion is MET or MISSED is decided by reading
these counts against the targets in criteria.md.

  1. completed all three tools and returned a fit card
  2. stopped early with a message, and no fit card
  3. the id in the branch step (session["selected_item"]) equals the id going
     into suggest_outfit, read from the trace
  4. the fit card contains: the price as a whole number (with or without "$"),
     the platform ignoring case, and a word from the title or a style_tag
     ignoring case
  5. every listing in search_results is priced at or below the ceiling N
"""

import re
import sys

from utils.data_loader import load_listings


def parse_report(path):
    """Return [{name, query, criterion, tries: [ {fields...} ]}] from a report."""
    import scenarios

    by_name = {s["name"]: s for s in scenarios.SCENARIOS}
    text = open(path, encoding="utf-8").read()
    body = text.split("## What actually happened", 1)[1]

    results = []
    for block in re.split(r"\n### ", body)[1:]:
        name = block.split("\n", 1)[0].strip()
        scenario = by_name[name]
        tries = []
        for t in re.split(r"\n\*\*Try \d+\*\*\n", block)[1:]:
            fit = re.search(r"Fit card:\n\n```\n(.*?)\n```", t, re.S)
            trace = re.search(r"Trace:\n\n```\n(.*?)\n```", t, re.S)
            crashed = re.search(r"Crashed:\n\n```\n(.*?)\n```", t, re.S)
            stopped = re.search(r"- stopped early: (.*)", t)
            selected = re.search(r"- selected_item: (.*?)(?: \(\$([\d.]+), (\w+)\))?$", t, re.M)
            count = re.search(r"- search_results: (\d+)", t)
            tries.append({
                "crashed": crashed.group(1) if crashed else None,
                "stopped": stopped.group(1) if stopped else "",
                "title": selected.group(1) if selected else "(none)",
                "fit_card": fit.group(1) if fit else None,
                "trace": trace.group(1) if trace else "",
                "count": int(count.group(1)) if count else None,
            })
        results.append({"name": name, "query": scenario["query"],
                        "criterion": scenario["criterion"], "tries": tries})
    return results


LISTINGS = {l["title"]: l for l in load_listings()}


def check_1(t):
    if t["crashed"]:
        return False, "crashed"
    if t["fit_card"]:
        return True, "fit card returned"
    return False, f"no fit card ({t['stopped'][:70]})"


def check_2(t):
    if t["crashed"]:
        return False, "crashed"
    stopped = t["stopped"].startswith("yes")
    if stopped and t["fit_card"] is None and "Try:" in t["stopped"]:
        return True, "stopped with a message naming what to change"
    return False, f"stopped={stopped}, fit_card={'set' if t['fit_card'] else 'None'}"


def check_3(t):
    branch = re.search(r"selected_item id=(\S+)", t["trace"])
    received = re.search(r"\[\d+\] suggest_outfit\n\s+in:\s+new_item id=([^,\s]+)", t["trace"])
    if not branch or not received:
        return False, "id missing from trace (run stopped before suggest_outfit)"
    a, b = branch.group(1), received.group(1)
    return a == b, f"selected {a} / suggest_outfit got {b}"


def check_4(t):
    card = t["fit_card"]
    if not card:
        return False, "no fit card"
    item = LISTINGS.get(t["title"])
    if item is None:
        return False, f"can't find listing {t['title']!r}"
    low = card.lower()
    price = f"{item['price']:g}"
    has_price = re.search(rf"(?<![\d.]){re.escape(price)}(?![\d])", card) is not None
    has_platform = item["platform"].lower() in low
    title_words = [w for w in re.findall(r"[a-z0-9']+", item["title"].lower())]
    has_word = (any(re.search(rf"\b{re.escape(w)}\b", low) for w in title_words)
                or any(tag.lower() in low for tag in item["style_tags"]))
    missing = [name for name, ok in (("price " + price, has_price),
                                     ("platform " + item["platform"], has_platform),
                                     ("title/tag word", has_word)) if not ok]
    return not missing, "all three present" if not missing else "missing: " + ", ".join(missing)


def check_5(t, query):
    # search_listings doesn't call the model, so the same parsed inputs always
    # return the same list. Re-run it from the inputs the trace recorded and
    # check every price, and that the count matches what the run saw.
    from tools import search_listings

    m = re.search(r"search_listings \(via MCP\)\n\s+in:\s+description='(.*?)', "
                  r"size=(None|'.*?'), max_price=(None|[\d.]+)", t["trace"])
    if not m:
        return False, "search step missing from trace"
    desc = m.group(1)
    size = None if m.group(2) == "None" else m.group(2).strip("'")
    ceiling = None if m.group(3) == "None" else float(m.group(3))
    if ceiling is None:
        return False, "no price ceiling was parsed from the query"
    results = search_listings(desc, size, ceiling)
    if len(results) != t["count"]:
        return False, f"re-run gave {len(results)} results, the run saw {t['count']}"
    over = [l["price"] for l in results if l["price"] > ceiling]
    prices = ", ".join(f"{l['price']:g}" for l in results)
    if over:
        return False, f"over ${ceiling:g}: {over}"
    return True, f"all {len(results)} at or under ${ceiling:g} ({prices})"


def main():
    path = sys.argv[1]
    for scenario in parse_report(path):
        n = scenario["criterion"]
        if n is None:
            continue
        marks = []
        print(f"\n[{n}] {scenario['name']}  —  {scenario['query']}")
        for i, t in enumerate(scenario["tries"], 1):
            ok, why = check_5(t, scenario["query"]) if n == 5 else \
                {1: check_1, 2: check_2, 3: check_3, 4: check_4}[n](t)
            marks.append("PASS" if ok else "FAIL")
            print(f"  try {i}: {'PASS' if ok else 'FAIL'} — {why}")
        print(f"  → {' | '.join(marks)}  ({marks.count('PASS')}/{len(marks)})")


if __name__ == "__main__":
    main()
