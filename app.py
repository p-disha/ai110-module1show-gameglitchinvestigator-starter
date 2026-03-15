import random
import streamlit as st
# FIX: Refactored all core game logic out of app.py into logic_utils.py using Claude Code Agent mode
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


def get_hot_cold(distance: int) -> str:
    """Return an emoji label based on how close a guess is to the secret."""
    if distance <= 3:
        return "🔥 Burning!"
    if distance <= 10:
        return "🌡️ Warm"
    if distance <= 20:
        return "🌥️ Cool"
    return "❄️ Freezing"


def hint_display(outcome: str, message: str, distance: int) -> None:
    """Render a color-coded hint banner with a Hot/Cold proximity badge."""
    hot_cold = get_hot_cold(distance)
    if outcome == "Win":
        st.success(f"{message}  •  {hot_cold}")
    elif outcome == "Too High":
        color_fn = st.warning if distance <= 10 else st.error
        color_fn(f"{message}  •  {hot_cold}")
    else:
        color_fn = st.warning if distance <= 10 else st.error
        color_fn(f"{message}  •  {hot_cold}")


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Stores structured per-guess data for the session summary table
if "history_detail" not in st.session_state:
    st.session_state.history_detail = []

st.subheader("Make a guess")

attempts_left = attempt_limit - st.session_state.attempts
st.info(f"Guess a number between {low} and {high}.  •  Attempts left: {attempts_left}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.history_detail = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

    # Show session summary even after game ends
    if st.session_state.history_detail:
        st.divider()
        st.subheader("📊 Session Summary")
        st.table(st.session_state.history_detail)

    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        distance = abs(guess_int - st.session_state.secret)

        if show_hint:
            hint_display(outcome, message, distance)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # Record structured row for the summary table
        st.session_state.history_detail.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess_int,
            "Outcome": outcome,
            "Proximity": get_hot_cold(distance),
            "Score After": st.session_state.score,
        })

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Live session summary table (visible while playing)
if st.session_state.history_detail:
    st.divider()
    st.subheader("📊 Session Summary")
    st.table(st.session_state.history_detail)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
