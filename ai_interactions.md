# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the assistant to add a persistent "high score" feature (Challenge 2): keep track of the best score across runs by saving it to a file, and surface it in the game's sidebar — without disturbing the existing rules or tests.

**What did the agent do?**

- Created a new module `high_score.py` with three small functions: `load_high_score()`, `save_high_score()`, and `update_high_score()`, storing the value in `high_score.json`.
- Wired it into `app.py`: a `st.sidebar.metric("🏆 Best score", load_high_score())` display, and a call to `update_high_score(...)` on a win, plus a "New best score!" note.
- Added `tests/test_high_score.py` covering a missing file, a save/load round-trip, the "only keep the best" rule, and a corrupt file.
- Added `high_score.json` to `.gitignore` so the runtime file doesn't get committed.

**What did you have to verify or fix manually?**

- The first idea read the file with no error handling; a missing or corrupted `high_score.json` would have crashed the app on startup. I had the assistant wrap the read in a `try/except` that returns `0` instead, and added the corrupt-file test to prove it.
- I made sure the tests use pytest's `tmp_path` fixture so they never touch the real `high_score.json` on my machine.
- I confirmed the whole suite still passed (`pytest`) and that the app launched cleanly after the change.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** *"Here are `logic_utils.py` and `app.py`. Suggest three edge-case inputs a player could enter that might still break the game, and write a pytest case for each that checks the game handles them gracefully."*

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`-5`) | (prompt above) | `test_negative_number_is_compared_numerically` | ✅ Pass | Players can type a minus sign; it should parse and read as "Too Low", not error. |
| Decimal (`49.9`) | (prompt above) | `test_decimal_input_is_truncated_to_int` | ✅ Pass | `parse_guess` accepts decimals by truncating, so I wanted to lock in that `49.9 → 49`. |
| Extremely large value (`999999999999`) | (prompt above) | `test_extremely_large_value_does_not_crash` | ✅ Pass | Python ints are unbounded, but I wanted proof a huge guess is just "Too High" with no overflow/crash. |
| Whitespace only (`"   "`) | follow-up: *"also test blank/whitespace input"* | `test_whitespace_only_input_is_rejected` | ✅ Pass | Spaces shouldn't count as a guess; should return the "Enter a guess." error. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Review app.py, logic_utils.py, high_score.py, and the tests for PEP 8
compliance. Run flake8, then fix any style/naming issues it reports.
```

**Linting output before:**

```
$ flake8 app.py logic_utils.py high_score.py conftest.py tests/
logic_utils.py:38:80: E501 line too long (81 > 79 characters)
tests/test_game_logic.py:9:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:14:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:19:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:32:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:37:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:42:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:47:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:51:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:66:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:72:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:78:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:90:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:94:1: E302 expected 2 blank lines, found 1
```

**Linting output after:**

```
$ flake8 app.py logic_utils.py high_score.py conftest.py tests/
(no output — clean)
```

**Changes applied:**

- **E501 (line too long):** shortened a docstring line in `logic_utils.py` ("explains why" → "says why") so it fits in 79 characters.
- **E302 (blank lines):** added a second blank line between top-level test functions, which is the PEP 8 convention. I accepted all of these because they're standard formatting, not behavior changes, and the tests still pass afterward.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

> **Note:** I compared two different *fix approaches* suggested for the same bug. (I wasn't able to run two separate vendor models side by side, so these are two distinct AI-suggested variants rather than, say, Claude vs. Gemini specifically.)

**Task given to both:** Fix the backwards-hint bug from Phase 1 — `check_guess` returned the right label but the wrong message ("Too High" → "Go HIGHER!").

| | Approach A (defensive) | Approach B (concise) |
|-|------------------------|----------------------|
| **Summary** | Keep `check_guess` returning a `(outcome, message)` tuple, add `try/except TypeError` to coerce types, and swap the messages inside the tuple. | Make `check_guess` return just the outcome string; coerce both sides to `int`; keep the player-facing text in a separate `hint_for()` lookup. |
| **More Pythonic?** | Less so — the `try/except` around comparisons hides type problems instead of preventing them, and bundling message + outcome mixes concerns. | More so — small single-responsibility functions, a dict lookup for messages, no exception-driven control flow. |
| **Clearer explanation?** | Explained the symptom ("messages are swapped") well. | Explained *why* the type bug happened (`"100" < "50"` as text) and why splitting outcome from message keeps the existing tests valid. |

**Which did you prefer and why?**

I went with **Approach B**. Approach A would have kept the fragile `try/except` comparison and forced me to rewrite the starter tests (which expect `check_guess(50, 50) == "Win"`, a plain string). Approach B fixed the root cause by comparing numerically, kept the original tests passing untouched, and separated "what's the outcome" from "what do we tell the player," which made the Hot/Cold UI feature easier to add later.
