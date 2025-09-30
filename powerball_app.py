import streamlit as st
import pandas as pd
from io import BytesIO
from st_aggrid import AgGrid

# ------------------------
# App Config
# ------------------------
st.set_page_config(page_title="Powerball Generator", layout="wide")

# ------------------------
# Example Data (replace with your logic)
# ------------------------
data = {
    "Ball-1": [5, 10, 20],
    "Ball-2": [12, 14, 22],
    "Ball-3": [23, 25, 30],
    "Ball-4": [33, 36, 40],
    "Ball-5": [45, 48, 50],
    "Powerball": [12, 18, 25]
}
combos_df = pd.DataFrame(data)

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
    label="Download as Excel",
    data=excel_file,
    file_name="powerball_combos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

