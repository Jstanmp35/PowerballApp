import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# --- Load historical data ---
def load_data(file_path="powerball_all.csv"):
    df = pd.read_csv(file_path)
    white_cols = [col for col in df.columns if 'Bal' in col or 'White' in col]
    return df, white_cols

try:
    df, white_cols = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Most common numbers ---
def most_common_numbers(df, cols, top_n=5):
    numbers = []
    for col in cols:
        numbers += df[col].tolist()
    count = pd.Series(numbers).value_counts().head(top_n)
    return count

st.subheader("Top 5 Most Common Historical White Balls")
st.write(most_common_numbers(df, white_cols, top_n=5))

# --- Number of combinations ---
num_combos = st.number_input(
    "Number of combinations to generate:", 
    min_value=1, max_value=50, value=10, step=1
)

# --- Generate combinations ---
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

if st.button("Generate Combinations"):
    top_combos = generate_unique_combos(num_combos)
    
    combos_df = pd.DataFrame(
        top_combos, 
        columns=['White1','White2','White3','White4','White5','Powerball']
    )

    # --- Display DataFrame without index ---
    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")
    st.dataframe(combos_df.style.set_properties(**{
        'text-align': 'center'
    }), height=400)

    # --- CSV Download ---
    csv_data = combos_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download combinations as CSV",
        data=csv_data,
        file_name="powerball_combinations.csv",
        mime="text/csv"
    )

    # --- Excel Download ---
    try:
        import io
        excel_file = io.BytesIO()
        combos_df.to_excel(excel_file, index=False, sheet_name='Powerball')
        st.download_button(
            label="Download combinations as Excel",
            data=excel_file.getvalue(),
            file_name="powerball_combinations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        st.warning("Excel download requires 'openpyxl'. Install it with pip install openpyxl.")

