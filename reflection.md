# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
 When I first ran the game, it looked like a normal number guessing game with a text box, a Submit button, and a sidebar for difficulty. Before I even made a guess, it said "Attempts left: 7" even though the sidebar said Normal allows 8 attempts, so I was already losing a turn. The hints were backwards: when I guessed 80 and the secret was 27, it told me "Go HIGHER," and when I guessed 10 it told me "Go LOWER." The strangest bug was when I guessed 100 on my 4th attempt and it said "Go LOWER," which was the opposite of what my guess of 80 got, even though both were too high. I also noticed my score went up after some wrong guesses, so the game didn't feel trustworthy at all.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|---|---|---|---|---|
| Start a game on Normal, no guesses yet | "Attempts left: 8" | "Attempts left: 7" | none | app.py, `st.session_state.attempts = 1` (should start at 0) |
| Guess 80, secret 27 | "Go LOWER" | "Go HIGHER" | none | app.py, `check_guess`: messages are swapped |
| Guess 10, secret 27 | "Go HIGHER" | "Go LOWER" | none | app.py, `check_guess`: messages are swapped |
| Guess 100, secret 27 (4th attempt) | Same hint as 80 (both too high) | Opposite hint | none | app.py, `if submit:` block, `attempts % 2 == 0` turns secret into a string, so the comparison is alphabetical |
| Wrong "too high" guesses on attempts 2 and 4 | Score goes down | Score went up +5 each | none | app.py, `update_score`, "Too High" branch |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
