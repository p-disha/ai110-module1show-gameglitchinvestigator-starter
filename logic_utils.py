from typing import Optional, Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return the inclusive numeric range for a given difficulty level.

    The range determines the pool of possible secret numbers the game
    will choose from. Higher difficulty levels use a wider range, making
    the secret harder to guess in fewer attempts.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.
            Any unrecognised value falls back to the Normal range.

    Returns:
        A tuple ``(low, high)`` representing the inclusive lower and
        upper bounds of the guessing range.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    # FIXME: Logic breaks here — Normal was 1–100 and Hard was 1–50, making Hard easier than Normal
    # FIX: Swapped ranges so Normal=1–50 and Hard=1–100; identified with Claude Code via codebase analysis
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: Optional[str]) -> Tuple[bool, Optional[int], Optional[str]]:
    """Parse and validate raw text input from the player into an integer guess.

    Accepts whole numbers and decimal strings (decimals are truncated toward
    zero, not rounded). Rejects empty, ``None``, or non-numeric input and
    returns a descriptive error message instead.

    Args:
        raw: The raw string the player typed into the input field.
            May be ``None`` if the widget has not been interacted with yet.

    Returns:
        A three-element tuple ``(ok, guess_int, error_message)`` where:

        - ``ok`` (``bool``): ``True`` if the input was valid, ``False`` otherwise.
        - ``guess_int`` (``int | None``): The parsed integer value when ``ok``
          is ``True``, otherwise ``None``.
        - ``error_message`` (``str | None``): A human-readable error string
          when ``ok`` is ``False``, otherwise ``None``.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> Tuple[str, str]:
    """Compare a player's guess against the secret number and return feedback.

    Determines whether the guess is correct, too high, or too low, and
    returns both a machine-readable outcome label and a human-readable
    hint message. Handles a TypeError fallback for cases where the secret
    is unexpectedly passed as a string.

    Args:
        guess: The integer value the player guessed.
        secret: The integer secret number chosen at the start of the game.

    Returns:
        A tuple ``(outcome, message)`` where:

        - ``outcome`` (``str``): One of ``"Win"``, ``"Too High"``,
          or ``"Too Low"``.
        - ``message`` (``str``): A short emoji-prefixed hint shown to
          the player (e.g. ``"📉 Go LOWER!"``).

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIXME: Logic breaks here — messages were swapped; too high should say Go LOWER
        # FIX: Corrected hint directions so Too High → Go LOWER and Too Low → Go HIGHER; fixed with Claude Code
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        guess_str = str(guess)
        if guess_str == secret:
            return "Win", "🎉 Correct!"
        if guess_str > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate a new score based on the outcome of a single guess attempt.

    Points are awarded on a win, scaled down by how many attempts were used.
    Wrong guesses may apply a penalty. The score never goes below zero as a
    result of this function (though callers are responsible for floor logic).

    Args:
        current_score: The player's score before this guess was evaluated.
        outcome: The result of the guess — one of ``"Win"``, ``"Too High"``,
            or ``"Too Low"``.
        attempt_number: The 1-based index of the current attempt (i.e. ``1``
            on the first guess, ``2`` on the second, and so on).

    Returns:
        The updated integer score after applying the outcome's point rules.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(100, "Too Low", 3)
        95
    """
    if outcome == "Win":
        # FIXME: Logic breaks here — (attempt_number + 1) adds an extra 10-point deduction
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIXME: Logic breaks here — wrong guesses should not reward points on even attempts
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
