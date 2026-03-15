from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1 fix: Hard difficulty range must be wider than Normal ---

def test_hard_range_is_wider_than_normal():
    # Hard was mistakenly 1–50, Normal was 1–100 — Hard should cover a larger range
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range upper bound ({hard_high}) should be greater than Normal ({normal_high})"
    )

def test_hard_range_upper_bound():
    # Hard range should go up to 100
    _, high = get_range_for_difficulty("Hard")
    assert high == 100

def test_normal_range_upper_bound():
    # Normal range should go up to 50
    _, high = get_range_for_difficulty("Normal")
    assert high == 50


# --- Bug 2 fix: hint messages must match the direction to guess ---

def test_too_high_message_says_go_lower():
    # When guess is above the secret, the hint must say Go LOWER, not Go HIGHER
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: '{message}'"

def test_too_low_message_says_go_higher():
    # When guess is below the secret, the hint must say Go HIGHER, not Go LOWER
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: '{message}'"


# --- Edge case 1: Negative numbers ---
# AI identified: parse_guess has no range validation, so negative numbers are accepted silently.
# A player typing "-5" gets ok=True and a "Too Low" hint instead of an error.

def test_negative_number_is_parsed():
    # "-5" currently parses successfully — documents that range validation is missing
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_negative_guess_is_too_low():
    # check_guess still gives a valid outcome for negative input
    outcome, _ = check_guess(-5, 50)
    assert outcome == "Too Low"


# --- Edge case 2: Decimal truncation ---
# AI identified: "3.7" is silently converted to 3 via int(float(raw)).
# The player receives no warning that their input was changed.

def test_decimal_is_truncated_not_rounded():
    # "3.7" becomes 3, not 4 — truncation, not rounding
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3, f"Expected 3 (truncated), got {value}"

def test_decimal_parse_returns_no_error():
    # No error message is returned, so the player is not warned of the truncation
    ok, _, err = parse_guess("3.7")
    assert ok is True
    assert err is None


# --- Edge case 3: Whitespace-only input ---
# AI identified: "   " bypasses the empty-string check and falls into int() conversion,
# returning "That is not a number." instead of the friendlier "Enter a guess."

def test_whitespace_only_is_rejected():
    # Whitespace-only should not be accepted as a valid guess
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None

def test_whitespace_only_returns_error_message():
    # Documents current behaviour: returns "That is not a number." rather than "Enter a guess."
    ok, _, err = parse_guess("   ")
    assert ok is False
    assert err is not None, "Expected an error message for whitespace-only input"
