def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low=None, high=None):
    """
    Parse user input into an int guess.

    If low and high are given, guesses outside low..high are rejected.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # FIX: Reject decimals instead of silently truncating them (e.g. "4.9" -> 4).
    if "." in raw:
        try:
            float(raw)
        except ValueError:
            return False, None, "That is not a number."
        return False, None, "Please enter a whole number."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: Reject guesses outside the difficulty's range (e.g. negatives).
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome: "Win", "Too High", or "Too Low"
    """
    # FIX: Removed the TypeError/string fallback; guess and secret are always ints now.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"

# FIX: Hint messages were swapped in app.py. Moved logic here with AI help and
# split hint text into its own function so "Too High" now says "Go LOWER".
def get_hint_message(outcome: str):
    """Return the hint message to show the player for a given outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Wrong guesses always cost 5 points (removed the even-attempt +5 bonus).
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
