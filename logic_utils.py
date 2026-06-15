"""Core game logic for the number guessing game.

Kept separate from app.py so the rules can be unit-tested without Streamlit.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the (low, high) inclusive guessing range for a difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """Parse raw text input into an integer guess.

    Returns (ok, guess_int, error_message).
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        # Accept "42" and also "42.0" by truncating to an int.
        value = int(float(text)) if "." in text else int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low".
    """
    # Compare as numbers so "100" is never treated as smaller than "50".
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for(outcome: str):
    """Return the player-facing hint message for an outcome.

    The arrow and direction match what the player should do next.
    """
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }
    return messages.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Add points for a win (more points for fewer attempts).

    A wrong guess never changes the score, so it can't drift negative.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    return current_score
