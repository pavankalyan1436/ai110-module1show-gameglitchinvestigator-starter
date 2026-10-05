from logic_utils import check_guess, get_hint_message, parse_guess

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

def test_too_high_hint_says_lower():
    # Guards against swapped hints: a guess above the secret must say "Go LOWER"
    assert "LOWER" in get_hint_message(check_guess(60, 50))

def test_too_low_hint_says_higher():
    # Guards against swapped hints: a guess below the secret must say "Go HIGHER"
    assert "HIGHER" in get_hint_message(check_guess(40, 50))

def test_three_digit_guess_vs_two_digit_secret():
    # Guards against string comparison: "100" < "27" alphabetically said "Too Low"
    assert check_guess(100, 27) == "Too High"

def test_one_digit_guess_vs_two_digit_secret():
    # Guards against string comparison: "9" > "50" alphabetically said "Too High"
    assert check_guess(9, 50) == "Too Low"

def test_parse_guess_strips_extra_spaces():
    # Edge case: copy-pasted input with surrounding spaces should still parse
    assert parse_guess("  42  ") == (True, 42, None)

def test_parse_guess_rejects_decimal():
    # Edge case: "4.9" is silently truncated to 4 instead of being rejected
    ok, value, err = parse_guess("4.9")
    assert ok is False

def test_parse_guess_rejects_negative():
    # Edge case: "-5" is below every difficulty's range but is accepted and costs an attempt
    ok, value, err = parse_guess("-5", 1, 100)
    assert ok is False
