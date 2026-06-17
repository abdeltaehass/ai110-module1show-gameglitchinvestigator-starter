"""Tiny file-backed high-score store for the guessing game.

The best score is persisted to a small JSON file so it survives app restarts.
File access is isolated here, away from the pure rules in ``logic_utils.py``.
"""

import json
import os

DEFAULT_PATH = "high_score.json"


def load_high_score(path=DEFAULT_PATH):
    """Return the saved high score, or 0 if none is stored yet.

    A missing or unreadable file is treated as "no high score" rather than an
    error, so the game always has a usable number to show.

    Args:
        path: Location of the JSON store.

    Returns:
        The stored high score as an int (0 when unavailable).
    """
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return int(data.get("high_score", 0))
    except (ValueError, OSError, TypeError):
        return 0


def save_high_score(score, path=DEFAULT_PATH):
    """Write ``score`` to the store and return it.

    Args:
        score: The score to persist.
        path: Location of the JSON store.

    Returns:
        The score that was written, as an int.
    """
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"high_score": int(score)}, handle)
    return int(score)


def update_high_score(score, path=DEFAULT_PATH):
    """Persist ``score`` only if it beats the stored high score.

    Args:
        score: The latest finished-game score.
        path: Location of the JSON store.

    Returns:
        The current high score after the update (an int).
    """
    best = load_high_score(path)
    if score > best:
        return save_high_score(score, path)
    return best
