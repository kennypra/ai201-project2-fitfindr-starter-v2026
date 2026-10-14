"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    # ── Criterion 3: state ────────────────────────────────────────────────────
    # "For 5 different queries..." — one scenario per query. Checked in the
    # trace: the id in the branch step vs the id going into suggest_outfit.
    {"name": "c3 state q1", "query": "denim jacket under $50",
     "wardrobe": "example", "criterion": 3},
    {"name": "c3 state q2", "query": "black combat boots",
     "wardrobe": "example", "criterion": 3},
    {"name": "c3 state q3", "query": "plaid flannel shirt",
     "wardrobe": "example", "criterion": 3},
    {"name": "c3 state q4", "query": "y2k baby tee",
     "wardrobe": "example", "criterion": 3},
    {"name": "c3 state q5", "query": "wide-leg trousers under $40",
     "wardrobe": "example", "criterion": 3},

    # ── Criterion 4: fit card ─────────────────────────────────────────────────
    # Same 5 different queries. Each card is checked for the price as a whole
    # number, the platform, and a word from the title or style_tags.
    {"name": "c4 fit card q1", "query": "denim jacket under $50",
     "wardrobe": "example", "criterion": 4},
    {"name": "c4 fit card q2", "query": "black combat boots",
     "wardrobe": "example", "criterion": 4},
    {"name": "c4 fit card q3", "query": "plaid flannel shirt",
     "wardrobe": "example", "criterion": 4},
    {"name": "c4 fit card q4", "query": "y2k baby tee",
     "wardrobe": "example", "criterion": 4},
    {"name": "c4 fit card q5", "query": "wide-leg trousers under $40",
     "wardrobe": "example", "criterion": 4},

    # ── Criterion 5: price ceiling ────────────────────────────────────────────
    # 5 different queries, each stating a ceiling; all four phrasings appear.
    # Every listing in search_results must be priced at or below N.
    {"name": "c5 ceiling 'under'", "query": "graphic tee under $25",
     "wardrobe": "example", "criterion": 5},
    {"name": "c5 ceiling 'less than'", "query": "denim jacket less than $45",
     "wardrobe": "example", "criterion": 5},
    {"name": "c5 ceiling 'below'", "query": "boots below $60",
     "wardrobe": "example", "criterion": 5},
    {"name": "c5 ceiling 'max'", "query": "flannel max $30",
     "wardrobe": "example", "criterion": 5},
    {"name": "c5 ceiling 'under' 2", "query": "cargo pants under $28",
     "wardrobe": "example", "criterion": 5},
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
