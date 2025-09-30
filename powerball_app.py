import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Powerball Number Generator",
    layout="wide"
)

st.title("Powerball Number Generator")

# --- Function to generate combinations ---
def generate_combinations(n=10):
    combos = []
    for _ in range(n):
        whites = sorted(random.sample(range(1, 70), 5))
        powerball = random.randint(1, 26)
        combos.append(whites + [powerball])
    return combos

# --- Generate combinations ---
num_combos = st.number_input("Number of combinations to generate:", min_value=1, max_value=100, value=10)
combos = generate_combinations(num_combos)

# --- Create DataFrame ---
columns = ["White1", "White2", "White3", "White4", "White5", "Powerball"]
combos_df = pd.DataFrame(combos, columns=columns)

# --- Display table WITHOUT index ---
st.table([dict(zip(combos_df.columns, row)) for row in combos_df.values])

# --- Download as Excel ---
def convert_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Powerball")
    processed_data = output.getvalue()
    return processed_data

excel_data = convert_to_excel(combos_df)
st.download_button(
    label="Download combinations as Excel",
    data=excel_data,
    file_name="powerball_combinations.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


