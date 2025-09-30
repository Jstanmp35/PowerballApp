\import streamlit as st
import pandas as pd
import random
import qrcode
import io

st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# Load historical data (replace with your CSV loading logic)
def load_data():
    # Example: replace with your actual CSV path
    df = pd.read_csv("powerball_all.csv")
    white_cols = ['Bal-1', 'Bal-2', 'Bal-3', 'Bal-4', 'Bal-5']
    return df, white_cols

# Function to get top most common numbers
def most_common_numbers(df, cols, top_n=5):
    counts = pd.Series(df[cols].values.ravel()).value_counts()
    return counts.head(top_n)

try:
    df, white_cols = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.subheader("Top 5 Most Common Historical White Balls")
st.write(most_common_numbers(df, white_cols, top_n=5))

# Number of combinations
num_combos = st.number_input("Number of combinations to generate:", min_value=1, max_value=50, value=10, step=1)

# Generate unique combinations
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
    
    combos_df = pd.DataFrame(top_combos, columns=['White1','White2','White3','White4','White5','Powerball'])
    combos_df.reset_index(drop=True, inplace=True)

    st.subheader(f"Generated {len(top_combos)} Powerball Combinations")
    st.dataframe(combos_df.style.set_properties(**{'text-align': 'center'}), height=400)

    # CSV download
    csv_data = combos_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download combinations as CSV",
        data=csv_data,
        file_name="powerball_combinations.csv",
        mime="text/csv"
    )

    # QR code generation
    APP_URL = "https://share.streamlit.io/Jstanmp35/PowerballApp/main/powerball_app.py"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(APP_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    st.image(buf, caption="Scan to open Powerball Generator on your phone", use_container_width=True)

