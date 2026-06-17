# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  A small number guessing game built with Streamlit. The app picks a secret number from a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–200). You type a guess and the game tells you whether it's too high, too low, or correct, while tracking your score and remaining attempts. You win by finding the number before you run out of attempts.

- [x] **Detail which bugs you found.**
  - Hints were backwards — a guess that was too high told you to "Go HIGHER!".
  - Every even-numbered guess was judged wrong because the secret was compared as text, so `"100"` counted as smaller than `"50"`.
  - The score drifted negative and sometimes went *up* after a wrong guess.
  - "New Game" didn't restart a finished round (status, score, and history were never reset) and ignored the difficulty range.
  - The "Attempts left" counter was off by one, and the prompt always said "between 1 and 100" no matter the difficulty.

- [x] **Explain what fixes you applied.**
  - Moved the game rules (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`, plus a new `hint_for`) out of `app.py` into `logic_utils.py` so they can be unit-tested.
  - Compared guesses to the secret numerically and corrected the hint direction.
  - Reworked scoring so only a win adds points (more for fewer attempts) and wrong guesses never change the score.
  - Made "New Game" fully reset state and respect the difficulty range, fixed the off-by-one attempts counter, and showed the real range in the prompt.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (secret = 50), followed in order:

1. The app loads and shows: "Guess a number between 1 and 100. Attempts left: 8".
2. User enters `40` → game returns **Too Low** with the hint "📈 Go HIGHER!". Attempts left drops to 7.
3. User enters `70` → game returns **Too High** with the hint "📉 Go LOWER!". Attempts left drops to 6.
4. User enters `60` → **Too High** again ("📉 Go LOWER!"). The score stays the same, because wrong guesses don't move it. Attempts left drops to 5.
5. User enters `50` → **🎉 Correct!** Balloons appear, the app reveals the secret, and the final score is shown.
6. User clicks **New Game 🔁** → a fresh secret is drawn from the current difficulty's range, attempts reset to 0, and the board is ready to play again.

**Screenshot** *(optional)*: _N/A — see the text walkthrough above._

## 🧪 Test Results

I completed **Challenge 1: Advanced Edge-Case Testing** — beyond the original three cases, the suite covers the hint direction, numeric-vs-text comparison (the `100` vs `50` bug), scoring behavior, rejecting non-numeric input, and tricky inputs like negatives, decimals, huge numbers, and whitespace. It also covers the Hot/Cold proximity labels and the high-score store.

```
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.11.4, pytest-9.1.0, pluggy-1.6.0
rootdir: .
collected 20 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  5%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 10%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 15%]
tests/test_game_logic.py::test_large_guess_is_too_high PASSED            [ 20%]
tests/test_game_logic.py::test_check_guess_handles_string_secret PASSED  [ 25%]
tests/test_game_logic.py::test_hint_points_player_the_right_way PASSED   [ 30%]
tests/test_game_logic.py::test_wrong_guess_does_not_change_score PASSED  [ 35%]
tests/test_game_logic.py::test_first_guess_win_scores_full PASSED        [ 40%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numbers PASSED    [ 45%]
tests/test_game_logic.py::test_negative_number_is_compared_numerically PASSED [ 50%]
tests/test_game_logic.py::test_decimal_input_is_truncated_to_int PASSED  [ 55%]
tests/test_game_logic.py::test_extremely_large_value_does_not_crash PASSED [ 60%]
tests/test_game_logic.py::test_whitespace_only_input_is_rejected PASSED  [ 65%]
tests/test_game_logic.py::test_proximity_exact_is_bullseye PASSED        [ 70%]
tests/test_game_logic.py::test_proximity_close_is_hot PASSED             [ 75%]
tests/test_game_logic.py::test_proximity_far_is_freezing PASSED          [ 80%]
tests/test_high_score.py::test_missing_file_reads_as_zero PASSED         [ 85%]
tests/test_high_score.py::test_save_then_load_roundtrip PASSED           [ 90%]
tests/test_high_score.py::test_update_only_keeps_the_best PASSED         [ 95%]
tests/test_high_score.py::test_corrupt_file_reads_as_zero PASSED         [100%]

============================== 20 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [x] **Challenge 1 — Advanced Edge-Case Testing.** Added tests for negatives, decimals, extremely large values, and whitespace-only input (see the Test Results above and `tests/test_game_logic.py`).

- [x] **Challenge 2 — Feature Expansion: persistent high score.** Added `high_score.py` (`load_high_score`, `save_high_score`, `update_high_score`) which saves the best score to `high_score.json`. `app.py` shows it in the sidebar (`st.sidebar.metric("🏆 Best score", ...)`) and calls `update_high_score(...)` when you win.

- [x] **Challenge 3 — Documentation & Linting.** Every function in `logic_utils.py` and `high_score.py` has a full Args/Returns docstring, and the code passes `flake8` with no findings.

- [x] **Challenge 4 — Enhanced Game UI.** The game now gives structured, friendly feedback:
  - **Color-coded directional hints** in `app.py` — "Too High" renders as a red `st.error("📉 Go LOWER!")` and "Too Low" as a blue `st.info("📈 Go HIGHER!")`.
  - **Hot/Cold temperature read-out** powered by the new `proximity_label(guess, secret, low, high)` in `logic_utils.py`, which returns labels like `🎯 Bullseye`, `🔥 Boiling hot`, `♨️ Hot`, `🌤️ Warm`, `❄️ Cold`, or `🧊 Freezing` (thresholds scale with the difficulty's range).
  - **Session summary table** rendered with `st.table(...)` at the bottom of `app.py`, listing each Guess, Result, and Closeness for the current game, and staying visible after the game ends.

- [x] **Challenge 5 — AI Model Comparison.** See the comparison write-up in `ai_interactions.md`.
