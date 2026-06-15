from logic_utils import check_guess, hint_for, update_score, parse_guess

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
