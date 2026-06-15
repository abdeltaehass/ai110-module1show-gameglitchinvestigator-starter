# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it (`python -m streamlit run app.py`), the game *looked* totally normal: a title, a sidebar with a Difficulty dropdown and an attempts counter, a "Developer Debug Info" expander that reveals the secret number, and a text box with **Submit Guess**, **New Game**, and a **Show hint** checkbox. The problems only showed up once I actually started playing. I opened the debug panel so I could see the secret, then guessed numbers on purpose to test the hints — and that's when things fell apart.

The biggest issue is that **the hints are backwards**. When I guessed a number higher than the secret it correctly figured out "Too High," but the message told me to "📈 Go HIGHER!" — the exact opposite of what I should do. On top of that, **every second guess gives a completely wrong hint** no matter what I type, because on even-numbered attempts the code compares my guess to the secret as text instead of as numbers (so 100 gets treated as smaller than 50). I also noticed the **score drifts negative** after a couple of wrong guesses and even *goes up* on some wrong answers, the **"New Game" button doesn't actually restart** the game once you've won or lost, and the **"Attempts left" counter starts one short** (it says 7 on Normal when the sidebar says 8 are allowed).

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Normal difficulty, secret = 50 (from debug panel), first guess = `60` | Hint should tell me to guess **lower** | Label was "Too High" but the message read "📈 Go HIGHER!" — pushes me the wrong way | none |
| On my **2nd** guess (even attempt), secret = 50, guess = `100` | "Too High" / hint to go lower | App said "📉 Go LOWER!" — it treats 100 as *smaller* than 50 | none (a `TypeError` is raised internally but silently caught, so no visible error) |
| Three wrong guesses in a row on Normal (e.g. `30`, `70`, `20`) | Score should stay sensible / never go below 0 | Score bounced +5 then −5 and ended up **negative** | none |
| Win or lose a round, then click **New Game 🔁** | Fresh game: counter resets, I can guess again | Still shows "Game over. Start a new game to try again." and blocks all input | none |
| Open the app on Normal (8 attempts allowed), before guessing | "Attempts left: 8" | Shows "Attempts left: 7" — off by one from the very start | none |
| Switch to **Easy** (range is 1–20) or **Hard** (1–50) | Prompt should show the real range | Prompt always says "Guess a number between 1 and 100" regardless of difficulty | none |

---

## 2. How did you use AI as a teammate?

I mostly worked with the AI chat assistant built into VS Code, and a couple of times I pasted a single function into ChatGPT for a second opinion. My habit was to attach both `app.py` and `logic_utils.py` so the assistant could see how the UI and the logic connected, then ask about **one bug at a time** instead of dumping the whole file on it.

**A suggestion that was correct:** When I asked why the hints felt backwards, the assistant pointed out that `check_guess` returned the right label ("Too High") but paired it with the wrong message ("📈 Go HIGHER!"), and suggested swapping the messages so "Too High" tells the player to go *lower*. That matched what I was seeing in the game, so I made the change and verified it two ways — a unit test asserting `"LOWER" in hint_for("Too High")`, and replaying the game where guessing 60 against a secret of 50 now correctly says "Go LOWER!".

**A suggestion that was misleading:** At one point the assistant wanted `check_guess` to keep returning a tuple `(outcome, message)` and to *rewrite the starter tests* to unpack it. That would have broken the existing test contract — `check_guess(50, 50) == "Win"` expects a plain string — so I turned it down. Instead I had `check_guess` return just the outcome string and moved the messages into a separate `hint_for()` helper. I confirmed this was the better call by running `pytest` and watching all nine tests pass without changing the original three.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could do two things: watch a test go from failing to passing, **and** reproduce the old broken behavior in the live app and see it behave correctly. For each fix I tried to write the smallest test that would have caught the original bug.

The clearest example was `test_large_guess_is_too_high`, which checks `check_guess(100, 50) == "Too High"`. This failed before the fix, because on even-numbered guesses the secret was turned into a string and `"100"` compared as *less than* `"50"` alphabetically — so the game called 100 "Too Low". After I switched `check_guess` to a numeric comparison, the test passed, which proved the type bug was gone. I also ran an end-to-end check with Streamlit's `AppTest` to play a full round (wrong guess → correct hint, right guess → win, New Game → fresh board) and confirmed no exceptions were raised.

AI helped me get started on the tests by suggesting the basic "60 vs 50 should be Too High" case. I extended that idea myself to cover the cases that had actually broken the game: the 100-vs-50 alphabetical-comparison bug, the hint direction, and a check that a wrong guess never changes the score.

---

## 4. What did you learn about Streamlit and state?

The biggest thing I learned is that Streamlit re-runs your *entire* script from top to bottom every time you interact with the page — every button click, text entry, or checkbox toggle starts the file over from line one. That means a normal variable gets recreated on every interaction, so anything you want to remember between clicks (the secret number, the score, how many attempts you've used) has to live in `st.session_state`, which Streamlit keeps around across reruns. I'd explain it to a friend like this: the script is like a recipe that gets re-cooked from scratch on every click, and `session_state` is the fridge where you store the ingredients you want to keep between cookings. A lot of the original bugs made more sense once I understood this — for example, the values that *were* in `session_state` (like the secret) survived correctly, but the per-click logic around them was where things went wrong.

---

## 5. Looking ahead: your developer habits

**One habit I want to keep:** writing a small test that *reproduces* a bug before I fix it. Seeing `test_large_guess_is_too_high` fail first and then pass gave me real proof the fix worked, instead of just assuming it did because the app "looked fine." I also want to keep committing in small, labeled steps (bugs logged, fixes applied, docs finished) so my history tells the story of what I did.

**One thing I'd do differently:** I'd give the AI more context up front and ask it about one bug at a time. Early on I asked broad questions and got broad, sometimes-wrong answers; the assistant was far more useful once I attached both files and pointed it at a specific symptom.

**How this changed how I think about AI-generated code:** I now treat AI output as a confident first draft, not a finished answer — it's great for spotting a likely cause or scaffolding a test, but it can also suggest changes that quietly break a working contract (like rewriting the starter tests), so I read every diff and verify with tests before trusting it.
