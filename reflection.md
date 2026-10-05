# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it looked like a normal number guessing game with a text box, a Submit button, and a sidebar for difficulty. Before I even made a guess, it said "Attempts left: 7" even though the sidebar said Normal allows 8 attempts, so I was already losing a turn. The hints were backwards: when I guessed 80 and the secret was 27, it told me "Go HIGHER," and when I guessed 10 it told me "Go LOWER." The strangest bug was when I guessed 100 on my 3rd guess and it said "Go LOWER," which was the opposite of what my guess of 80 got, even though both were too high. I also noticed my score went up after a wrong guess, so the game didn't feel trustworthy at all.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|---|---|---|---|---|
| Start a game on Normal, no guesses yet | "Attempts left: 8" | "Attempts left: 7" | none | app.py, `st.session_state.attempts = 1` (should start at 0) |
| Guess 80, secret 27 | "Go LOWER" | "Go HIGHER" | none | app.py, `check_guess`: messages are swapped |
| Guess 10, secret 27 | "Go HIGHER" | "Go LOWER" | none | app.py, `check_guess`: messages are swapped |
| Guess 100, secret 27 (3rd guess, attempt counter = 4) | Same hint as 80 (both too high) | Opposite hint ("Go LOWER") | none | app.py, `if submit:` block, `attempts % 2 == 0` turns secret into a string, so the comparison is alphabetical |
| Guess 80 (too high) on attempt 2 | Score goes down | Score went up +5 | none | app.py, `update_score`, "Too High" branch rewards even attempts |
| Submit a guess, then open Debug Info | Panel shows current attempts/history | Panel is one step behind (missing latest guess) | none | app.py, Debug Info expander is drawn before the `if submit:` block |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude inside VS Code as my coding assistant, plus Claude in a separate chat window as a step-by-step guide. One correct AI suggestion was its explanation of the even-attempt bug: it said that on even attempts the secret became the string "27", so guessing 100 fell back to a text comparison where "100" < "27" because '1' comes before '2'. I verified this by matching it to my real game: 80 → "Go HIGHER", 10 → "Go LOWER", and 100 → "Go LOWER" with secret 27 all lined up with its explanation.

One suggestion I did not accept as written was in my first bug table: the AI guide said both of my "too high" guesses (80 and 100) added +5 points. When the VS Code AI explained the logic, I saw that 100 was actually mislabeled "Too Low" and lost 5 points, so only 80 added +5, and I corrected that row myself. I also noticed that the first refactor kept the TypeError string fallback inside check_guess, so the string bug was still there; I didn't treat that as done and removed it in a separate, focused prompt.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I only counted a bug as fixed when two things were true: pytest passed and the live game behaved correctly when I replayed my Phase 1 inputs. For example, after removing the string conversion I guessed 100 twice in a row and both times got "Go LOWER", where before the second guess flipped. I ran `python -m pytest -v` after every change, and it went from 3 to 7 passing tests. The AI generated four new tests for hint direction and integer comparison, like `check_guess(100, 27) == "Too High"`. It also pointed out an honest limitation: since the string conversion used to happen in app.py, those tests confirm integer comparison works but wouldn't have caught the original bug on their own.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-runs the whole Python script from top to bottom every time you click a button or type something. That means normal variables get reset on every click, so anything the game needs to remember, like the secret, score, or attempts, has to live in `st.session_state`, which survives between reruns. I also learned that order matters: the Debug Info panel is drawn before the submit code runs, so it always showed values one step behind my latest guess.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

A habit I want to keep is writing down the exact input, expected result, and actual result before fixing anything; that bug table made it easy to check whether the AI's explanations were true. Next time I would give the AI one small, specific task per chat from the start and always say "do not modify the tests," because big vague prompts are harder to review. This project showed me that AI-generated code can look clean and still be quietly wrong, so I treat it as a draft that I have to verify, not as finished work.