import random

import streamlit as st

from high_score import load_high_score, update_high_score
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_for,
    parse_guess,
    proximity_label,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A number guessing game.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.sidebar.metric("🏆 Best score", load_high_score())

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# Count guesses made so far; the first guess takes this from 0 to 1.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

# Each entry is a row: {"Guess", "Result", "Closeness"}.
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# Show the real range for the chosen difficulty, not a hard-coded one.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # Reset everything so a finished game can actually be replayed,
    # and draw the new secret from the current difficulty's range.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

game_active = st.session_state.status == "playing"

if not game_active:
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

if submit and game_active:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # Invalid input shouldn't burn an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1

        # Compare against the real secret (an int), every attempt.
        outcome = check_guess(guess_int, st.session_state.secret)
        closeness = proximity_label(
            guess_int, st.session_state.secret, low, high
        )

        st.session_state.history.append({
            "Guess": guess_int,
            "Result": outcome,
            "Closeness": closeness,
        })

        if show_hint and outcome != "Win":
            # Color-code the direction: red for too high, blue for too low.
            if outcome == "Too High":
                st.error(hint_for(outcome))
            else:
                st.info(hint_for(outcome))
            st.caption(f"Temperature: {closeness}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            best = update_high_score(st.session_state.score)
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            if st.session_state.score >= best:
                st.caption("🏆 New best score!")
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

# Session summary table — stays visible even after the game ends.
if st.session_state.history:
    st.divider()
    st.subheader("📋 Session summary")
    st.table(st.session_state.history)

st.divider()
st.caption("A small Streamlit guessing game.")
