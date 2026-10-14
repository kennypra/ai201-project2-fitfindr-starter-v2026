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

## Failure Modes

Each failure triggered on purpose, with exactly what the agent printed.

**1. Empty search.** Handled by the branch in `agent.py::run_agent`; already
worked in unit 3, no change needed.

```
$ python app.py ask 'sequined wedding gown size XXS under $5'

  No listings matched "sequined wedding gown" in size XXS at or under $5. Try: raise the price ceiling above $5 or drop it; drop "size XXS" (sizes must match exactly, so M won't match S/M); use broader keywords, like a type of item (tee, jeans, jacket) or a style (vintage, y2k, streetwear).

0 model calls this session
```

**2. Empty wardrobe.** Handled in `tools.py::suggest_outfit`, which gives
general styling advice when `wardrobe["items"]` is empty; already worked in
unit 3, no change needed.

```
$ python app.py ask 'denim jacket under $50' --empty-wardrobe
(running with an empty wardrobe)

  Found:    Denim Jacket — Light Wash, Cropped — $42.0 on poshmark

  Outfit:   Layer that light wash denim jacket over a classic black baby tee, and pair them with high-waisted wide-leg trousers and retro white sneakers. Add a simple canvas tote bag and layered silver chains for an effortless, street-style ready look that balances vintage texture with modern comfort. 

For a relaxed off-duty vibe, throw the cropped jacket over an oversized grey hoodie and team it with black biker shorts. Finish the outfit with chunky athletic sneakers and a baseball cap to lean into an athletic streetwear aesthetic that is both cozy and chic.

  Fit card: Found this cropped light wash denim jacket on Poshmark for forty-two bucks and I am obsessed. It has that perfect worn-in vintage look without trying too hard. Tossed it on with some wide-leg trousers and a baby tee for an effortless street-style vibe.

2 model calls this session, 294 prompt + 166 output tokens
```

**3. Model unavailable.** Triggered with a bad key for one command
(`GEMINI_API_KEY=badkey123`, caching off); the real key in `.env` was never
changed.

Before the fix, `run_agent` raised `ModelUnavailable` and only the catch-all in
`app.py::main` stopped it. The search result was lost, and `run_eval.py` would
have recorded a crash:

```
ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

I added a `ModelUnavailable` handler in `agent.py::run_agent` around the two
model-calling tools. It puts a message in `session["error"]`, keeps the item the
search found, and leaves `fit_card` as `None`:

```
$ GEMINI_API_KEY=badkey123 AI201_CACHE=0 python app.py ask 'black leather boots under $60'

  Couldn't reach the style model, so there's no outfit or fit card. The search still found Platform Mary Janes — Black Patent ($55 on depop). Check GEMINI_API_KEY in .env, or try again in a minute if the model is busy.

1 model calls this session
```

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
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item's id is the id `suggest_outfit` receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card has the price as a number, the platform, and a title/tag word | 4 of 5 | FAIL | FAIL | FAIL | FAIL | PASS | MISSED (1/5) |
| 5. No result is over a stated price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**How the rows were filled.** Criteria 1 and 2 are one query, so Try 1–5 are
its five tries. Criteria 3, 4, and 5 say "5 different queries", so each has
five scenarios in `scenarios.py`, and each scenario also ran five times. In
the table, **Try N is query N's first try**, a rule fixed before reading the
results. All 25 runs for each are below, and no verdict changes with them:

| Criterion | Query 1 | Query 2 | Query 3 | Query 4 | Query 5 | All 25 runs |
|---|---|---|---|---|---|---|
| 3 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 25/25 |
| 4 | 2/5 | 0/5 | 0/5 | 2/5 | 3/5 | 7/25 |
| 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 25/25 |

Queries for 3 and 4: `denim jacket under $50`, `black combat boots`,
`plaid flannel shirt`, `y2k baby tee`, `wide-leg trousers under $40`.
Queries for 5: `graphic tee under $25`, `denim jacket less than $45`,
`boots below $60`, `flannel max $30`, `cargo pants under $28`.

**Real output from one try** per criterion: Try 1 of each criterion's first
scenario, from `results/run_2026-10-14_0019_before.md`. The run was driven by
`run_eval.py::main`, the loop is `agent.py::run_agent`, and the fit card text
comes from `tools.py::create_fit_card`.

*Criterion 1:* `vintage graphic tee under $30`, Try 1. Completed, fit card returned.

```
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

Fit card:
Found this little butterfly baby tee on Depop for eighteen bucks and it is pure early 2000s energy. It fits super snug and gives off major Lizzie McGuire vibes in the best way possible. Can not wait to wear this with some baggy denim and chunky sneakers all summer long.
```

*Criterion 2:* `designer ballgown size XXS under $5`, Try 1. Stopped at the branch.

```
- stopped early: yes — No listings matched "designer ballgown" in size XXS at or under $5. Try: raise the price ceiling above $5 or drop it; drop "size XXS" (sizes must match exactly, so M won't match S/M); use broader keywords, like a type of item (tee, jeans, jacket) or a style (vintage, y2k, streetwear).
- selected_item: (none)

[2] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
[3] branch
      out: No listings matched "designer ballgown" in size XXS at or under $5. Try: raise the price ceiling above $5 …
      →    search empty → stop before suggest_outfit
```

*Criterion 3:* `denim jacket under $50`, Try 1. The id in the branch step
matches the id going into `suggest_outfit`.

```
[3] branch
      out: selected_item id=lst_007 (Denim Jacket — Light Wash, Cropped)
      →    7 results → took the first
[4] suggest_outfit
      in:  new_item id=lst_007, wardrobe: 10 items
[5] create_fit_card
      in:  new_item id=lst_007, outfit from suggest_outfit
```

*Criterion 4:* `denim jacket under $50`, Try 1. FAIL: the price ($42.0) is
written in words.

```
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

Fit card:
Scored this light wash cropped denim jacket on Poshmark for forty-two bucks and it's already a staple. The wash has that perfectly broken-in look without actually feeling worn out. Gives off major 90s streetwear energy especially when thrown over a grey crewneck and some baggy jeans.

check_run.py: try 1: FAIL — missing: price 42
```

*Criterion 5:* `graphic tee under $25`, Try 1. All 4 results at or under $25.

```
[2] search_listings (via MCP)
      in:  description='graphic tee', size=None, max_price=25.0
      out: 4 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +1 more

check_run.py: try 1: PASS — all 4 at or under $25 (18, 24, 15, 19)
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
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | Counted tries whose session ended with a fit card and no error: 5 of 5, at or above 4. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | Every try ended with `session["error"]` naming what to change (price, size, keywords), `fit_card` `None`, and no `suggest_outfit` step in the trace. |
| 3 | The selected item's id is the id `suggest_outfit` receives | 5 of 5 | MET (5/5) | Compared the id in each trace's branch step with the id on the `suggest_outfit` input line: equal for all 5 queries, and in all 25 runs. |
| 4 | The fit card has the price as a number, the platform, and a title/tag word | 4 of 5 | MISSED (1/5) | `check_run.py` searched each card for all three: only 1 of the 5 queries' first tries passed (7 of all 25 runs), below 4. |
| 5 | No result is over a stated price ceiling | 5 of 5 | MET (5/5) | Re-ran `search_listings` on the inputs recorded in each trace, confirmed the result count matched the run, and checked every price was at or below N: 5 of 5. |

**Diagnoses**

**Criterion 4: MISSED (1/5). Step: the model's output in `tools.py::create_fit_card`. Mechanism: the prompt never says how to write the price.** It passes `Price: $42` and asks the model to "mention the item, price, and platform", while the system prompt asks it to sound like a real person posting. The model mentions the price every time, but usually spelling out the number: "forty-two bucks", "twenty-two bucks", "eighteen bucks". My criterion needs the number as digits, so those cards fail.

Evidence that this is the only cause:

- **It's one failure, not three.** Across every fit card in the run (85 cards,
  from all scenarios that reached `create_fit_card`), 68 failed the check and
  all 68 failed on the price. The platform and a title/tag word were present in
  85 of 85.
- **It isn't the tool, the branch, or the session.** The right item reached
  the tool every time: criterion 3's trace ids matched in 25 of 25 runs, and
  the price the model was given was correct (`$42` for the $42.0 jacket). The
  same item and prompt gave `$42` on some tries and "forty-two bucks" on
  others, which is the model choosing, not the code.
- **It's systematic, not occasional.** Digits showed up only 17 times in 85
  cards, and some items never got them: the $22 flannel had digits in 2 of 25
  cards, and the $44 boots and $27 cargo pants in 0 of 5 each.

That also shows my target's reasoning was wrong. I allowed one miss in five for
"model variation", but this is not random variation. The prompt leaves the
format open, and the casual voice I asked for pulls it toward words almost
every time.



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
$ python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query (regex)
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] branch
      out: selected_item id=lst_002 (Y2K Baby Tee — Butterfly Print)
      →    10 results → took the first
[4] suggest_outfit
      in:  new_item id=lst_002, wardrobe: 10 items
      out: Pair the Y2K Baby Tee — Butterfly Print with your baggy straight-leg jeans and chunky white sneakers for an ef…
[5] create_fit_card
      in:  new_item id=lst_002, outfit from suggest_outfit
      out: Scored this cute little butterfly tee on Depop for just 18 bucks. It has the ultimate 2000s mallrat energy wit…
```

**Empty search**

```
$ python app.py ask 'sequined wedding gown size XXS under $5' --trace

[1] parse_query (regex)
      in:  sequined wedding gown size XXS under $5
      out: description='sequined wedding gown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  description='sequined wedding gown', size='XXS', max_price=5.0
      out: [] (empty)
[3] branch
      out: No listings matched "sequined wedding gown" in size XXS at or under $5. Try: raise the price ceiling above $5 …
      →    search empty → stop before suggest_outfit
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

`search_listings` now runs on an MCP server (`mcp_server.py`), and
`agent.py::run_agent` calls it with `call_tool("search_listings", {...})`
instead of calling the function directly; the other two tools are still direct
calls. Nothing behaved differently afterwards: on four test queries (including
one with no matches) the MCP results were identical to the direct call, and the
empty case still came back as `[]`, not `None`. The tool already returned plain
lists of plain dicts, so nothing was lost on the way through MCP.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** One prompt, in `tools.py::create_fit_card`. I added one
sentence to the end of the user prompt telling the model how to write the price:

```
Before:
  "Write the caption. Mention the item, price, and platform and be specific
   about the vibe it gives off."

After:
  "Write the caption. Mention the item, price, and platform and be specific
   about the vibe it gives off. Write the price exactly as {price}, in digits,
   never spelled out in words."
```

`{price}` is the item's real price, e.g. `$42`. In the same prompt I also added
the missing spaces between the system prompt's sentences, which had been
running together (`"...thrift finds.Sound like a real person..."`). Nothing
else changed: same tools, loop, scenarios, temperature (0.9), and caching off.

**Which failure it was meant to fix:** Criterion 4. The diagnosis showed every
failed fit card failed for one reason: the model wrote the price in words
("forty-two bucks") because the prompt never said what format to use.

### Run Log — After

Run with `python run_eval.py --label after` (same 18 scenarios, 5 tries each,
caching off, 170 model calls). Raw output:
`results/run_2026-10-14_0050_after.md`, marked by `check_run.py`. Rows are
filled the same way as before: Try N is query N's first try for criteria 3–5.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item's id is the id `suggest_outfit` receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card has the price as a number, the platform, and a title/tag word | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. No result is over a stated price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

| Criterion | Before (first tries) | After (first tries) | Before (all 25 runs) | After (all 25 runs) |
|---|---|---|---|---|
| 4 | 1/5 MISSED | 5/5 MET | 7/25 | 25/25 |

Real output, criterion 4, `denim jacket under $50`, Try 1 (the same scenario
and try pasted in the before log):

```
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

Fit card:
Scored this light wash cropped denim jacket on Poshmark for $42 and I am obsessed. It gives off such a cool, effortless vintage streetwear vibe. Can't wait to style it with everything from baggy jeans to khaki trousers.

check_run.py: try 1: PASS — all three present
```

**Did it help, and how do I know:** Yes: criterion 4 went from MISSED (1/5)
to MET (5/5), and every fit card in the whole after-run (85 of 85, across all
scenarios) wrote the price in digits, up from 17 of 85 before, while criteria
1, 2, 3, and 5 stayed at 5/5. I read all 25 criterion-4 cards by hand to
confirm `check_run.py`'s marks; the cards still read like real posts ("for
only $42 and I'm honestly obsessed"). One caveat: the spacing fix went into
the same run, so the two can't be fully separated, but the spacing change says
nothing about the price, and the price was the only thing that failed.

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
