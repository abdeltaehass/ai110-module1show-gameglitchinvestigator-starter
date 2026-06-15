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

I also completed **Challenge 1: Advanced Edge-Case Testing** — beyond the original three cases, the suite covers the hint direction, numeric-vs-text comparison (the `100` vs `50` bug), scoring behavior, and rejecting non-numeric input.

```
$ pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.11.4, pytest-9.1.0, pluggy-1.6.0
rootdir: .
collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 33%]
tests/test_game_logic.py::test_large_guess_is_too_high PASSED            [ 44%]
tests/test_game_logic.py::test_check_guess_handles_string_secret PASSED  [ 55%]
tests/test_game_logic.py::test_hint_points_player_the_right_way PASSED   [ 66%]
tests/test_game_logic.py::test_wrong_guess_does_not_change_score PASSED  [ 77%]
tests/test_game_logic.py::test_first_guess_win_scores_full PASSED        [ 88%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numbers PASSED    [100%]

============================== 9 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
