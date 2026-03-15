# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
It was a guessing game with debugger info section to know the secret and try guessing it. The game was buggy.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1.The hints were opposite of what they shoud have been for eg when a number was entered which was higher than the secret it should give the hint -go lower (instead of the buggy go higher).
2. Hard(1,50) difficulty is easier than normal(1,100).
3. New Game resets to 0 , but startup begins at 1, making the first attempt count as the second. This also makes "Attempts left" display off by one at the start.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). go higher go lower bug was correct by ai, it swapped the logic
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
For Hard range AI suggested the range 1,200 but I told AI to keep the range for Hard as 1,100 and change the normal range to 1,50

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
using pytest and writing the tests for that bug and also using the ui by playing the game.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
  I ran pytest on test_game_logic.py after the fixes. The test test_too_high_message_says_go_lower checked that when a guess is above the secret, the message contains "LOWER". Before the fix this test would have failed because the original code returned "Go HIGHER!" for a too-high guess. Seeing it pass confirmed that the hint logic was correctly reversed.
- Did AI help you design or understand any tests? How?
  Yes. Claude Code wrote the pytest cases targeting both bugs specifically — it explained that check_guess returns a tuple (outcome, message), which is why the existing tests were also broken (they compared the full tuple to a bare string). AI suggested checking the message content with "LOWER" in message rather than an exact string match, which made the test more readable and less brittle.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Every time you click a button or change an input in a Streamlit app, the entire Python script reruns from top to bottom — it is not like a normal program that waits for events. Because of this, any regular variable you set would be reset on each rerun and the game would forget your score and attempts instantly. Session state is a dictionary that Streamlit keeps alive between reruns, so values like the secret number, attempt count, and score survive each refresh. In this project, initializing session state with `if "secret" not in st.session_state` made sure a new secret was only generated once per game instead of on every button click.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Writing pytest cases that specifically target a known bug before and after fixing it. This gave me a concrete way to verify each fix rather than just eyeballing the UI, and it means if the bug ever comes back the test will catch it immediately. I also want to keep separating logic from UI code from the start rather than refactoring it out later.
- What is one thing you would do differently next time you work with AI on a coding task?
  I would give the AI clearer constraints upfront instead of correcting it after the fact — for example, specifying the exact range values I wanted for difficulty levels rather than letting AI choose 1–200 and then having to redirect it. Being precise in the prompt saves a round trip and keeps me more in control of the decisions.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  I used to assume AI-generated code was either fully correct or obviously broken, but this project showed me it can be subtly wrong in ways that look plausible — like difficulty ranges that compile and run fine but have the hard and normal levels backwards. Now I treat AI output as a first draft that always needs a human to read it critically and verify the logic, not just check that it runs.
