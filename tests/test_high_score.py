from high_score import load_high_score, save_high_score, update_high_score


def test_missing_file_reads_as_zero(tmp_path):
    path = tmp_path / "scores.json"
    assert load_high_score(str(path)) == 0


def test_save_then_load_roundtrip(tmp_path):
    path = str(tmp_path / "scores.json")
    save_high_score(80, path)
    assert load_high_score(path) == 80


def test_update_only_keeps_the_best(tmp_path):
    path = str(tmp_path / "scores.json")
    assert update_high_score(50, path) == 50   # first score sets the bar
    assert update_high_score(30, path) == 50   # lower score doesn't replace it
    assert update_high_score(90, path) == 90   # higher score wins
    assert load_high_score(path) == 90


def test_corrupt_file_reads_as_zero(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text("not valid json")
    assert load_high_score(str(path)) == 0
