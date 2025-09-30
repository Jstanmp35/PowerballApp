import streamlit as st
from powerball_ai import load_data, most_common_numbers
import pandas as pd
import random
import io

st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# Load historical data
try:
    df, white_cols = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.subheader("Top 5 Most Common Historical White Balls")
st.write(most_common_numbers(df, white_cols, top_n=5))

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

# Generate combinations when button is clicked
if st.button("Generate Combinations"):
    top_combos = generate_unique_combos(num_combos)
    
    combos_df = pd.DataFrame(
        top_combos, 
        columns=['White1','White2','White3','White4','White5','Powerball']
    )
    combos_df.reset_index(drop=True, inplace=True)  # remove index completely

    # Console print clean
    print(combos_df.to_string(index=False))

    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")

    # Web table (Markdown, index-free)
    markdown_table = combos_df.to_markdown(index=False)
    st.markdown(markdown_table)

    # Excel-ready download
    excel_file = io.BytesIO()
    combos_df.to_excel(excel_file, index=False, sheet_name='Powerball')
    excel_file.seek(0)
    st.download_button(
        label="Download combinations as Excel",
        data=excel_file,
        file_name="powerball_combinations.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
