import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# Load historical data
def load_data():
    try:
        df = pd.read_csv("powerball_all.csv")
        # Detect white ball columns automatically
        white_cols = [col for col in df.columns if "Bal" in col or "White" in col]
        return df, white_cols
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df, white_cols = load_data()

# Number of combinations to generate
num_combos = st.number_input(
    "Number of combinations to generate:", 
    min_value=1, max_value=50, value=10, step=1
)

def generate_unique_combos(num_combos):
    """Generate Powerball combinations with no repeated white balls across all combos."""
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

if st.button("Generate Combinations"):
    top_combos = generate_unique_combos(num_combos)
    
    combos_df = pd.DataFrame(
        top_combos, 
        columns=['White1','White2','White3','White4','White5','Powerball']
    )
    # Reset index to avoid index column in display
    combos_df.reset_index(drop=True, inplace=True)

    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")

    # Excel-style display (centered, no index)
    st.dataframe(
        combos_df.style.set_properties(**{
            'text-align': 'center',
            'border': '1px solid black'
        }), 
        height=400
    )

    # CSV download without index
    csv_data = combos_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download combinations as CSV",
        data=csv_data,
        file_name="powerball_combinations.csv",
        mime="text/csv"
    )



