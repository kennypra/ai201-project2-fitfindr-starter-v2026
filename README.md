# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a clothes thrifting agent that we built in Unit 3 and will test in unit 4: the user types what they want in plain NL (e.g., `vintage graphic tee under $30, size M`) and the agent pulls generates a description, size, and price ceiling and searches  through listings from different platforms. If something matches, it takes the best match, suggests outfits that pair it from pieces from a wardrobe (or general styling advice if  wardrobe is empty), and writes a short caption they could post. If nothing matches, it stops and tells the user what to change.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** searches the listings for items that match the input description 
(optional: size and price ceiling)
- **Inputs:** `description` (str), `size` (str), and  `max_price` (float)
- **Returns:** a list of matching listing dicts (ranked best match first). Each dict has the 
following fields: id, title, description, category, style_tags (list), size, condition, price 
(float), colors (list), brand (str or None), platform
- **When it has nothing:** returns an empty list when there's no match

### `suggest_outfit`

- **What it does:** given an item and a wardrobe, the function suggests one or two outfits
- **Inputs:** `new_item` (dict) and `wardrobe` (dict)
- **Returns:** a non-empty string with outfit suggestions
- **When it has nothing:** if the wardrobe is empty, the function simply provides general 
styling advice

### `create_fit_card`

- **What it does:** generates a short caption someone would post about the thrift find
- **Inputs:**  `outfit` (str) and `new_item` (dict)
- **Returns:** a 2-4 sentence caption of the thrift find
- **When it has nothing:** if `outfit` is empty/whitespace, return a descriptive message 

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in
`session["error"]` that suggests what changes the user could make (e.g., raise/drop the
price, change the size, use broader keywords in description), return the session,
and stop without calling `suggest_outfit`. Otherwise, take the first result (i.e., best
match) as `session["selected_item"]` and go to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. A dollar amount after "under" (e.g.
`under $30`) is `max_price` (float). The word after "size" (e.g. `size M`) is `size`. 
Both are removed from the query and whatever that remains is the `description`. If 
either of the patterns are missing, that particular input is `None` and the filter is skipped.

**What moves through the session:** (1) `parsed` (description, size, max_price) -> (2) `search_results` (from `search_listings`) -> (3) `selected_item` (first result) -> (4) `outfit_suggestion` (from `suggest_outfit`) -> (5)`fit_card` (from `create_fit_card`). 
If search empty, only `parsed`, `search_results` (empty), and `error` are set -> 
`selected_item`, `outfit_suggestion`, and `fit_card` stay `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit:   Pair the Y2K Baby Tee — Butterfly Print with your baggy straight-leg jeans and chunky white sneakers for an effortless early-2000s streetwear look. Layer the vintage black denim jacket over top and sling the black crossbody bag across your chest to tie the casual, nostalgic vibe together.

For a sweet mix of edgy and soft, style the Y2K Baby Tee — Butterfly Print with your wide-leg khaki trousers, defined at the waist by the brown leather belt. Slip into your black combat boots and toss the black cropped zip hoodie over your shoulders or wear it unzipped to add a cool, contrasting finish to the pastel butterfly graphics.

Fit card: Scored this cute little butterfly tee on Depop for just 18 bucks. It has the ultimate 2000s mallrat energy without looking like a costume. Can't wait to throw it on with somebaggy denim and chunky sneakers for running errands.

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'],'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Pair your new Vintage Levi's 501 Jeans with the white ribbed tank top tucked in, accented by the brown leather belt. Throw on the black cropped zip hoodie and finish the look with chunkywhite sneakers and the black crossbody bag for an effortless, casual streetwear vibe.

For a cool, textured denim-on-denim look, wear the Vintage Levi's 501 Jeans with the oversized grey crewneck sweatshirt layered underneath the vintage black denim jacket. Ground the outfit with the black combat boots and keep your essentials in the black crossbody bag.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi 501s on Depop for thirty eight bucks and they fit like an absolute dream. The medium wash gives off such an effortless nineties dad vibe. Just threw them on with my beat-up white sneakers and honestly I'm never taking them off.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to review my five criteria and reasons and tell me how it would test each one using only the sentence.
- *What came back:* For criterion #4, it pointed out that I was checking for "a word naming the item's category", but categories are values like `tops` and `bottoms`, and a caption about a tee will say "tee", not "tops". So the check would fail on good captions. It also asked what counts as the price (`$18` vs `18.0`) and whether "Depop" counts for `depop`.
- *What I changed:* I replaced category with "a word from the item's title or style_tags", and decided the price counts as a whole number with or without `$`, and the platform match ignores case.

**Moment 2**

- *What I asked for:* I asked Claude to build `search_listings` with the size rule I picked: exact match, ignoring case.
- *What came back:* The tool, plus a test showing that `'graphic tee'` in size `M` under $30 returns nothing, because every graphic tee in the data is listed as `S/M` or `L`. It recommended whole-token matching instead, so `M` would match `S/M`. It had also put an import and a stopword list at the top of `tools.py`.
- *What I changed:* I kept exact match on purpose and wrote it into my Tool Inventory (`M` does not match `S/M`), and had the import and stopwords moved inside the function so all my changes stay inside the tool. Running the full agent later showed the cost: `vintage graphic tee under $30, size M` returned a floral slip dress, because one shared word ("vintage") is enough to count as a match.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
