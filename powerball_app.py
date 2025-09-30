import streamlit as st
import pandas as pd
import random
from io import BytesIO
import qrcode
from PIL import Image
from powerball_ai import load_data, most_common_numbers

# --- Page Setup ---
st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# --- Load Historical Data ---
try:
    df, white_cols = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Display Top 5 Historical White Balls ---
st.subheader("Top 5 Most Common Historical White Balls")
st.table(most_common_numbers(df, white_cols, top_n=5))

# --- Number of Combinations Input ---
num_combos = st.number_input(
    "Number of combinations to generate:", 
    min_value=1, max_value=50, value=10, step=1
)

# --- Generate Unique Powerball Combinations ---
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

# --- Generate Button ---
if st.button("Generate Combinations"):
    top_combos = generate_unique_combos(num_combos)
    
    combos_df = pd.DataFrame(
        top_combos, 
        columns=['White1','White2','White3','White4','White5','Powerball']
    )
    combos_df.reset_index(drop=True, inplace=True)

    # --- Excel-style Styling with Alternating Row Colors ---
    def excel_style(val):
        return 'text-align: center; border: 1px solid #d3d3d3; padding: 5px;'

    row_colors = [
        {'selector': f'tr:nth-child({i+2})',
         'props': [('background-color', '#f9f9f9')]} if i % 2 == 0 else
        {'selector': f'tr:nth-child({i+2})',
         'props': [('background-color', 'white')]} 
        for i in range(len(combos_df))
    ]

    styled_df = combos_df.style.set_table_styles(
        [
            {'selector': 'th', 
             'props': [('text-align', 'center'),
                       ('background-color', '#f0f0f0'),
                       ('border', '1px solid #d3d3d3'),
                       ('padding', '5px')]}
        ] + row_colors
    ).applymap(excel_style)

    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")
    st.dataframe(styled_df, height=400, use_container_width=True)

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
        excel_file = BytesIO()
        combos_df.to_excel(excel_file, index=False, sheet_name='Powerball')
        st.download_button(
            label="Download combinations as Excel",
            data=excel_file.getvalue(),
            file_name="powerball_combinations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        st.warning("Excel download requires 'openpyxl'. Make sure it's in requirements.txt")

# --- QR Code Section ---
st.subheader("Open this app on your phone")

# Replace this with your actual deployed Streamlit app URL
app_url = "https://share.streamlit.io/Jstanmp35/PowerballApp/main/powerball_app.py"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=8,
    border=4,
)
qr.add_data(app_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
st.image(img, caption="Scan to open Powerball Generator on your phone", use_column_width=False)
st.markdown(f"[Or click here to open the app]({app_url})")
