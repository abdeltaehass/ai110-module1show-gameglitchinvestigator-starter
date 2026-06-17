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

**Task given to both models:** I pasted the original buggy `check_guess` from Phase 1 into two assistants with the same prompt — the hint was backwards ("Too High" but "Go HIGHER!") and it behaved unreliably on some turns — and asked each to fix it and explain why the fix works.

| | Model A — ChatGPT | Model B — Claude |
|-|-------------------|------------------|
| **Fix returned** | Swapped only the hint messages ("Too High" → "📉 Go LOWER!", "Too Low" → "📈 Go HIGHER!") in *both* the normal path and the `try/except` fallback. Left the overall structure (the `try/except` and the `str()` fallback) unchanged. | Coerced `guess` and `secret` to `int()` at the top (with a guard that returns an error on bad input), deleted the string-comparison fallback entirely, and used a clean `if/elif/else` with the corrected messages. |
| **More Pythonic?** | Less so — it keeps the convoluted `try/except` and the `str()` fallback, so the underlying type bug is still lurking; it only patches the symptom (the text). | More so — converting to `int` up front removes the exception-driven control flow and the buggy fallback, leaving a short, readable function. (This is the same direction I took in my own fix.) |
| **Clearer explanation?** | Accurate and honest: it correctly noted the comparison logic was already right and only the messages were swapped, and it openly admitted the snippet shows no turn-based logic, so it *couldn't* explain the "even-numbered turns" symptom. | More complete on the "why": it explained the message swap **and** traced the unreliable turns to a type mismatch (`int` vs `str`) that raised a `TypeError` the original `except` block mishandled — though it made some assumptions about how inputs were captured. |

**Which did you prefer and why?**

I preferred **Claude's (Model B)** fix. ChatGPT correctly fixed the visible symptom — the swapped hint text — and was refreshingly honest that it couldn't explain the even-turn glitch from the snippet alone. But it left the brittle `try/except` + string-comparison structure in place, which is exactly what caused the type bug in the first place. Claude went after the root cause by comparing numerically and removing the fallback, which is both more Pythonic and the same approach I used in the project. The trade-off: Claude's explanation was more thorough but slightly speculative about input handling, while ChatGPT stuck strictly to what the code actually proved.
