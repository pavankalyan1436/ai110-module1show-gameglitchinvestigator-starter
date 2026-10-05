# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest -v`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"?
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** Move the logic into `logic_utils.py`, run `pytest`, and keep fixing until all tests pass.

## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number guessing game. The player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), then guesses a secret number within a limited number of attempts. After each guess the game gives a "Go HIGHER" / "Go LOWER" hint and updates the score. Fewer attempts to win means a higher score.

- [x] **Bugs I found:**
  1. **Hints were backwards:** a guess above the secret said "Go HIGHER" and a guess below said "Go LOWER" (`check_guess` in `app.py`).
  2. **Secret compared as text on even attempts:** `app.py` turned the secret into a string when `attempts % 2 == 0`, so numbers were compared alphabetically (`"100" < "27"`). The same guess could get opposite hints on different turns.
  3. **Lost one attempt at the start:** `attempts` started at 1, so Normal showed "Attempts left: 7" instead of 8.
  4. **Wrong guesses could add points:** `update_score` gave +5 for "Too High" guesses on even attempts.
  5. **New Game didn't fully reset:** it didn't reset status, score, or history, and always picked a secret from 1–100 regardless of difficulty. The info box also always said "1 and 100".
  6. **The secret did not actually change on every Submit** in my copy. It was already stored in `st.session_state`, so I verified this claim from the mission list instead of assuming it was true.

- [x] **Fixes I applied:**
  1. Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` from `app.py` into `logic_utils.py`, and imported them in `app.py`.
  2. Changed `check_guess` to return only the outcome (`"Win"`, `"Too High"`, `"Too Low"`) and added `get_hint_message(outcome)` so "Too High" says "Go LOWER" and "Too Low" says "Go HIGHER".
  3. Removed the even-attempt string conversion and the `TypeError` string fallback, so the game always compares integers.
  4. Started `attempts` at 0 so the player gets the full attempt limit.
  5. Made wrong guesses always cost 5 points.
  6. Made New Game reset attempts, score, status, and history, and pick the secret from the current difficulty's range. The info box now shows the real range.
  7. `parse_guess` now rejects decimals and out-of-range numbers, and invalid input no longer uses up an attempt (Challenge 1).

- **Known issue:** if you change difficulty in the middle of a game, the old secret stays until you click New Game. The Debug Info panel also shows values one step behind, because it is drawn before the submit logic runs.

## 📸 Demo Walkthrough

1. Start the app on **Normal**. The info box says "Guess a number between 1 and 100. Attempts left: 8".
2. The secret is 27 (visible in Developer Debug Info). The user types **4.9**, and the game shows "Please enter a whole number." Attempts left stays at 8.
3. The user guesses **80**, and the game shows "📉 Go LOWER!" and the score drops by 5.
4. The user guesses **100**, and the game again shows "📉 Go LOWER!" (before the fix, this flipped to the opposite hint).
5. The user guesses **10**, and the game shows "📈 Go HIGHER!" and the score drops by 5 again.
6. The user guesses **27**, balloons appear, and the game shows "You won! The secret was 27" with the final score.
7. The user clicks **New Game**, and attempts, score, and history reset. The user can play again.

## 🧪 Test Results

```
$ python -m pytest -v
collected 10 items

tests/test_game_logic.py::test_winning_guess PASSED                           [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                          [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                           [ 30%]
tests/test_game_logic.py::test_too_high_hint_says_lower PASSED                [ 40%]
tests/test_game_logic.py::test_too_low_hint_says_higher PASSED                [ 50%]
tests/test_game_logic.py::test_three_digit_guess_vs_two_digit_secret PASSED   [ 60%]
tests/test_game_logic.py::test_one_digit_guess_vs_two_digit_secret PASSED     [ 70%]
tests/test_game_logic.py::test_parse_guess_strips_extra_spaces PASSED         [ 80%]
tests/test_game_logic.py::test_parse_guess_rejects_decimal PASSED             [ 90%]
tests/test_game_logic.py::test_parse_guess_rejects_negative