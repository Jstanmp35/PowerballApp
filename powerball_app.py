import streamlit as st
import pandas as pd
import random
from io import BytesIO
from st_aggrid import AgGrid

# ------------------------
# App Config
# ------------------------
st.set_page_config(page_title="Powerball Generator", layout="wide")

# ------------------------
# Generate Powerball Numbers
# ------------------------
def generate_combinations(n=10):
    combos = []
    for _ in range(n):
        white_balls = random.sample(range(1, 70), 5)  # 5 unique numbers 1–69
        white_balls.sort()
        powerball = random.randint(1, 26)  # 1 number 1–26
        combos.append(white_balls + [powerball])
    df = pd.DataFrame(combos, columns=["White1", "White2", "White3", "White4", "White5", "Powerball"])
    return df

# ------------------------
# User Input
# ------------------------
st.title("🎰 Powerball Number Generator")
num_combos = st.slider("How many combinations?", 5, 50, 10)

# ------------------------
# Generate Data
# ------------------------
combos_df = generate_combinations(num_combos)

# ------------------------
# Show Table without Index
# ------------------------
st.subheader("Generated Powerball Numbers")
st.dataframe(combos_df.reset_index(drop=True), use_container_width=True)

# ------------------------
# Interactive Table (AgGrid)
# ------------------------
st.subheader("Interactive Table")
AgGrid(combos_df)

# ------------------------
# Download as Excel
# ------------------------
excel_file = BytesIO()
combos_df.to_excel(excel_file, index=False, sheet_name="Powerball")
st.download_button(
    label="📥 Download as Excel",
    data=excel_file,
    file_name="powerball_combos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

