"""Core game logic for the number guessing game.

These functions are kept separate from ``app.py`` so the rules can be
unit-tested without starting Streamlit. Every function here is pure: it takes
plain values and returns plain values, with no Streamlit or file-system calls.
"""


def get_range_for_difficulty(difficulty):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        A ``(low, high)`` tuple. Unknown values fall back to ``(1, 100)``.
    """
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw):
    """Parse raw text input into an integer guess.

    Accepts plain integers (``"42"``) and decimal strings (``"42.0"``), which
    are truncated to an int. Surrounding whitespace is ignored.

    Args:
        raw: The raw string from the input box (may be ``None`` or empty).

    Returns:
        A ``(ok, guess_int, error_message)`` tuple. On success ``ok`` is
        ``True`` and ``error_message`` is ``None``; on failure ``ok`` is
        ``False``, ``guess_int`` is ``None``, and ``error_message`` says why.
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        value = int(float(text)) if "." in text else int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret and return the outcome.

    Both values are coerced to ``int`` first, so a guess of ``100`` is never
    treated as smaller than ``50`` the way a text comparison would be.

    Args:
        guess: The player's guess (int, or anything int-convertible).
        secret: The secret number (int, or anything int-convertible).

    Returns:
        One of the strings ``"Win"``, ``"Too High"``, or ``"Too Low"``.
    """
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for(outcome):
    """Return the player-facing hint message for an outcome.

    The arrow and wording match what the player should do next, e.g.
    ``"Too High"`` tells the player to go *lower*.

    Args:
        outcome: An outcome string from :func:`check_guess`.

    Returns:
        A short hint string, or ``""`` for an unknown outcome.
    """
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }
    return messages.get(outcome, "")


def proximity_label(guess, secret, low, high):
    """Return a "Hot/Cold" style label for how close a guess is.

    The thresholds scale with the size of the range, so the same labels stay
    meaningful on Easy (1-20) and on Hard (1-200).

    Args:
        guess: The player's guess.
        secret: The secret number.
        low: The lowest value in the current range.
        high: The highest value in the current range.

    Returns:
        A short label such as ``"🎯 Bullseye"``, ``"🔥 Boiling hot"``,
        ``"♨️ Hot"``, ``"🌤️ Warm"``, ``"❄️ Cold"``, or ``"🧊 Freezing"``.
    """
    guess = int(guess)
    secret = int(secret)
    span = max(1, int(high) - int(low))
    distance = abs(guess - secret)
    ratio = distance / span

    if distance == 0:
        return "🎯 Bullseye"
    if ratio <= 0.05:
        return "🔥 Boiling hot"
    if ratio <= 0.15:
        return "♨️ Hot"
    if ratio <= 0.30:
        return "🌤️ Warm"
    if ratio <= 0.50:
        return "❄️ Cold"
    return "🧊 Freezing"


def update_score(current_score, outcome, attempt_number):
    """Update the running score after a guess.

    A win adds points, with more points awarded for fewer attempts. Any other
    outcome leaves the score unchanged, so it can never drift negative.

    Args:
        current_score: The score before this guess.
        outcome: An outcome string from :func:`check_guess`.
        attempt_number: How many guesses have been made this game (1-based).

    Returns:
        The updated score as an int.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    return current_score
