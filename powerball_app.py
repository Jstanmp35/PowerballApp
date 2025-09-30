import streamlit as st
import pandas as pd
import random

# --- Page setup ---
st.set_page_config(page_title="Powerball Number Generator", layout="centered")
st.title("Powerball Number Generator")

# --- Number of combinations ---
num_combos = st.number_input(
    "Number of combinations to generate:", 
    min_value=1, max_value=50, value=10, step=1
)

# --- Generate Powerball combinations ---
def generate_unique_combos(num_combos):
    used_whites = set()
    combos = []
    attempts = 0
    max_attempts = num_combos * 100

    while len(combos) < num_combos and attempts < max_attempts:
        white_balls = random.sample(range(1, 70), 5)
        if all(n not in used_whites for n in white_balls):
            powerball = random.randint(1, 26)
            combos.append((*sorted(white_balls), powerball))
            used_whites.update(white_balls)
        attempts += 1

    if len(combos) < num_combos:
        st.warning("Could not generate all unique combos without repeating white balls.")
    return combos

# --- Generate button ---
if st.button("Generate Combinations"):
    top_combos = generate_unique_combos(num_combos)
    
    combos_df = pd.DataFrame(
        top_combos, 
        columns=['White1','White2','White3','White4','White5','Powerball']
    )

    # --- Display table without index numbers ---
    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")
    st.table(combos_df)  # st.table automatically hides the index

    # --- CSV download ---
    csv_data = combos_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download combinations as CSV",
        data=csv_data,
        file_name="powerball_combinations.csv",
        mime="text/csv"
    )
