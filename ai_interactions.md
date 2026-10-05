# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:**

```
Suggest three edge-case inputs for parse_guess that might still break the game (for example negative numbers, decimals, extremely large values, or extra spaces). For each, explain in one line why it's risky.

Then add pytest cases for them to tests/test_game_logic.py. If a test reveals a real bug, tell me before changing logic_utils.py. Do not change existing tests. Run pytest afterwards.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| `"  42  "` (extra spaces) | Edge-case prompt above | `parse_guess("  42  ")` returns `(True, 42, None)` | ✅ Passed right away | Pasted input often has spaces around it; I wanted to make sure that doesn't block a valid guess. Python's `int()` already trims spaces. |
| `"4.9"` (decimal) | Edge-case prompt above | `parse_guess("4.9")` is rejected | ❌ Failed at first (returned 4), ✅ passes after fix | `int(float())` silently cut 4.9 to 4, so the player was judged on a number they never typed. I chose to reject decimals with "Please enter a whole number." |
| `"-5"` (out of range) | Edge-case prompt above, then my decision prompt | `parse_guess("-5", 1, 100)` is rejected | ❌ Failed at first (accepted -5), ✅ passes after fix | No difficulty allows numbers below 1, but it was accepted and used up an attempt. I chose to add optional `low`/`high` parameters to `parse_guess` so the range check stays testable and the existing tests don't break. |

**Human-in-the-loop decisions:** The AI found the two bugs but stopped and asked me how to handle them instead of guessing. I decided on rejecting decimals and range-checking inside `parse_guess`. The AI also pointed out that invalid input still used up an attempt, and I told it to fix that by only incrementing attempts after a valid guess.

**Result:** All 10 tests pass. In the game, `4.9`, `-5`, and `abc` show an error and no longer cost an attempt.