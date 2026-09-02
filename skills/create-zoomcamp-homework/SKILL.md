---
name: create-zoomcamp-homework
description: Create a Zoomcamp module homework (multiple-choice, reproducible) in Alexey's style. Use when asked to write or draft homework for a course module - finding what the workshop deferred, building on the previous homework, generating reproducible data, and matching the established voice.
---

# Create Zoomcamp Homework

Use this when writing a homework for a Zoomcamp course module (e.g. the
`llm-zoomcamp` repo, `cohorts/<year>/<NN-module>/homework.md`).

The goal: a short, multiple-choice homework that makes students re-do the
module's main ideas on a slightly different dataset, with reproducible answers.
Follow the steps below. They encode how Alexey likes these built and the
corrections he has made before - apply them up front so they don't have to be
made again.

## 1. Find what the workshop left for homework

Each module is a live workshop, chopped into per-lesson pages. The workshop
often defers a piece explicitly: "I'll leave this as homework", "we won't cover
X today", "the approach is similar, do it yourself".

- Get the workshop recording link from the module `README.md` ("Original
  workshop recording"), fetch its transcript (fetch-youtube skill), and save it
  to `.tmp/<videoid>-<module>-workshop.txt`.
- Grep the transcript for: `homework`, `exercise`, `leave (it|this) (to you|as
  homework)`, `for you`, `on your own`, `we won't|I won't cover`, `skip`.
- The deferred piece is the core of the homework. Cross-check the previous
  homework's closing lines - they often point forward ("you'll do exactly that
  in the <next> homework").

Report what you found before building, and confirm the angle.

## 2. Build it as a continuation of the previous homework

Homeworks chain. Reuse the previous homework's dataset and code so students keep
working in the same project.

- Same knowledge base (for `llm-zoomcamp`: the course lessons pulled via
  `gitsource` at the pinned commit `8c1834d`, the 72 lesson pages).
- Same derived objects (chunks, indexes, search functions) - reference them as
  "from homework N" instead of re-deriving.
- Open the intro by naming the link: "In homework N we built X and ended with an
  open question ... that's what we do here."

## 3. Question structure

Six questions, `Q1`..`Q6`, same as the other homeworks. Each question is a `##`
heading, a short prompt, then a bullet list of options.

- **Q1 is hands-on but cheap.** Have students run the module's main technique
  (e.g. LLM question generation) on just a *few* documents (3 is fine) so they
  don't spend money. Ask about something deterministic - e.g. the **average
  input tokens** across those few calls. Grade on input tokens (the prompt size
  is the same for everyone); note that output tokens vary by model/provider and
  to pick the closest option.
- **Then switch to pre-generated data.** Say "you don't need to generate the
  rest - we already did it the same way as in the lessons" and give a `wget` for
  a committed data file. Q2..Q6 run on this file so answers are reproducible.
- Cover the deferred technique. For evaluation that meant: a single-query
  sanity check (Q2/Q3 - run search for the first ground-truth question, report
  the top result's label), then aggregate metrics (Q4 hit rate, Q5 MRR), then a
  tuning question.
- **Make the last question interesting.** Sweep a parameter and ask which value
  is best (e.g. RRF `k` over `1, 50, 100, 200` - spread the values far apart).
  When ties are likely, add: "Several values may give the same result. If
  there's a tie, pick the smallest."

## 4. Reproducible data

- Generate the full dataset once, with the same approach the lessons use.
- Commit it next to the homework: `cohorts/<year>/<NN-module>/<name>.csv`.
- `wget` it from `main`:
  `https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/cohorts/<year>/<NN-module>/<name>.csv`
- The committed file fixes the answers. Never regenerate it once committed -
  generation is non-deterministic and would change `ground_truth[0]` and every
  downstream answer.

## 5. How much code to show

Default to prose; show code only for what's new or easy to get wrong. The
homework continues the module, so students already have the lesson code.

Show:
- New/important constructs (e.g. the chunking call, the `rrf` function, a new
  search wrapper).
- The generation **instructions** (the prompt text) - keep these visible so the
  homework is reproducible.

Don't show (describe in prose, or reference the lesson):
- Client setup (`OpenAI()`, `load_dotenv()`).
- Re-defining classes/helpers the lesson already defined - say "use the same
  `Questions` model and `llm_structured` from the lesson" instead of pasting.
- Loops over data for a question - name the documents/filenames instead.
- Boilerplate like `pd.read_csv(...).to_dict(...)` - say "load it with pandas
  into `ground_truth`".
- Index-building that just repeats the previous homework - describe it.

When you do show code:
- No inline function calls as arguments - assign to a variable first
  (`text_results = text_search(q)` then `rrf([text_results, ...])`).
- Put distinct definitions in their own code blocks (e.g. `rrf` and the function
  that uses it are two blocks, with a one-line lead-in each).
- One blank line between definitions inside a block, not two.

## 6. Answer options

- Token counts: order-of-magnitude spread (`140 / 1400 / 14000 / 140000`).
- Metrics (hit rate, MRR): a plausible spread around the real value
  (`0.55 / 0.66 / 0.76 / 0.88`); compute the real number, pick the closest as
  the key.
- File/label answers: the real one plus 3 plausible neighbours (use the actual
  top-5 of the relevant search to pick realistic distractors).
- Always end the homework with: "It's possible your answers won't match exactly.
  If so, select the closest one."

## 7. Voice and style

Match the existing homeworks (`cohorts/2026/01-agentic-rag`, `02-vector-search`)
and run the `stylint` skill. The accepted homeworks already "fail" stylint on
structural items that are inherent to this file type - that's the baseline, not
a target to beat:

- Q&A prompts are questions (`prose-question`, `question-opener`).
- Learning-in-public uses `###` sub-headings, ``` code blocks for the posts,
  `@mentions` (third-person/name), and a bare submit URL.
- The "We encourage everyone to share..." paragraph is fixed boilerplate.

Fix the *non-structural* findings in your own prose: long clauses (split into
two sentences), `lead-in-multi` (make the colon sentence its own one-liner
before a code block), `count-list` ("two metrics: ..." -> name them or bullet),
banned words (`shape` -> `structure`/`format`), question-word headings,
`repeated-and` chains, flat copular definitions ("The only change is X" -> "We
change only X"), and colon-introduced inline lists.

Also (project conventions, from `[[avoid-word-twist]]`): never use the word
"twist"; no bold markup in homework/lesson prose. Don't over-narrate the
answer - state the question and stop; Alexey removes "and so X is the best..."
wrap-up paragraphs.

Use `-` for em-dash-style asides (the repo uses hyphen, not `—`). Recommend
`gpt-5.4-mini` but say any model/provider works - "just adapt the client".

## 8. Reuse the standard sections

Copy the **Learning in Public** and **Submit the results** sections from an
existing 2026 homework. Update the module number/title and the four `✅` bullets
in the LinkedIn post and the X post. Keep the submit URL pointing at the right
`hwN`.

## 9. Solution workflow

Work in `.tmp/` (gitignored), never `tmp/` (tracked):

- Build a lab: `.tmp/<hwN>lab/` with `uv`, the embedder, the model (symlink the
  cached HuggingFace model to avoid re-downloading), and a `.env`.
- Write `solve.py` that computes every answer; run it once to generate and save
  the data file, then copy that file to `cohorts/.../`.
- Save `solve.py` and a `solution.md` (answer table + per-question detail) to
  `.tmp/<hwN>/`.
- Verify answers against the *committed* data file. For parameter sweeps, write
  a small script that reads the committed file rather than regenerating.

## 10. Final structure

```
## Homework: <Module>
<intro: continuation of homework N + what we measure here>
> It's possible your answers won't match exactly. If so, select the closest one.

## Setup            <- continues hw N; extra libs; load data
## <generate data>  <- prose + the instructions prompt; reference lesson helpers
## Q1               <- hands-on on a few docs; token usage; provider-variance note
## <full data>      <- "we already generated it"; wget the committed file
## <build search>   <- chunk code + prose; rrf + hybrid code blocks
## Q2..Q6           <- single-query checks, then metrics, then a tuning sweep
## <closing note>   <- the framework generalizes (no over-narration)
## Learning in Public
## Submit the results
```
