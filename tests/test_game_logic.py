from logic_utils import (
    check_guess,
    hint_for,
    update_score,
    parse_guess,
    proximity_label,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Tests for the bugs fixed in Phase 2 ---

def test_large_guess_is_too_high():
    # Guards the old bug where 100 vs 50 was compared as text and
    # came back "Too Low" because "100" < "50" alphabetically.
    assert check_guess(100, 50) == "Too High"


def test_check_guess_handles_string_secret():
    # Even if a value arrives as text, it should be compared numerically.
    assert check_guess(100, "50") == "Too High"
    assert check_guess("9", 50) == "Too Low"


def test_hint_points_player_the_right_way():
    # "Too High" must tell the player to go LOWER, and vice versa.
    assert "LOWER" in hint_for("Too High")
    assert "HIGHER" in hint_for("Too Low")


def test_wrong_guess_does_not_change_score():
    # Wrong guesses should never push the score around (or negative).
    assert update_score(0, "Too High", 3) == 0
    assert update_score(0, "Too Low", 4) == 0


def test_first_guess_win_scores_full():
    # Winning on the first attempt should award the maximum.
    assert update_score(0, "Win", 1) == 100


def test_parse_guess_rejects_non_numbers():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- Challenge 1: advanced edge-case inputs ---

def test_negative_number_is_compared_numerically():
    # A negative guess is below any positive secret, not a crash.
    ok, value, _ = parse_guess("-5")
    assert ok is True and value == -5
    assert check_guess(-5, 50) == "Too Low"


def test_decimal_input_is_truncated_to_int():
    # "49.9" should parse as 49 and read as Too Low against 50.
    ok, value, _ = parse_guess("49.9")
    assert ok is True and value == 49
    assert check_guess(value, 50) == "Too Low"


def test_extremely_large_value_does_not_crash():
    # A huge number is just Too High; no overflow, no exception.
    ok, value, _ = parse_guess("999999999999")
    assert ok is True
    assert check_guess(value, 50) == "Too High"


def test_whitespace_only_input_is_rejected():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


# --- Challenge 4: Hot/Cold proximity labels ---

def test_proximity_exact_is_bullseye():
    assert proximity_label(50, 50, 1, 100) == "🎯 Bullseye"


def test_proximity_close_is_hot():
    # 2 away on a span of ~99 is within the boiling-hot band.
    assert "hot" in proximity_label(52, 50, 1, 100).lower()


def test_proximity_far_is_freezing():
    assert proximity_label(1, 100, 1, 100) == "🧊 Freezing"
