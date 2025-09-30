import streamlit as st
import pandas as pd
import random

# Page config
st.set_page_config(page_title="Powerball Generator", layout="centered")
st.title("Powerball Number Generator (Excel-Style Display)")

# Load historical data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("powerball_all.csv")
    except FileNotFoundError:
        st.error("CSV file 'powerball_all.csv' not found!")
        st.stop()
    white_cols = [col for col in df.columns if "Bal" in col or "White" in col]
    return df, white_cols

@st.cache_data
def most_common_numbers(df, white_cols, top_n=5):
    numbers = []
    for col in white_cols:
        numbers += df[col].tolist()
    counts = pd.Series(numbers).value_counts()
    return counts.head(top_n)

df, white_cols = load_data()

st.subheader("Top 5 Most Common Historical White Balls")
st.write(most_common_numbers(df, white_cols, top_n=5))

# Input: number of combinations
num_combos = st.number_input(
    "Number of combinations to generate:", 
    min_value=1, max_value=50, value=10, step=1
)

# Generate Powerball combinations
def generate_combos(n):
    combos = []
    for _ in range(n):
        whites = sorted(random.sample(range(1, 70), 5))
        powerball = random.randint(1, 26)
        combos.append(whites + [powerball])
    return combos

# Generate button
if st.button("Generate Combinations"):
    combos = generate_combos(num_combos)
    combos_df = pd.DataFrame(
        combos,
        columns=['White1', 'White2', 'White3', 'White4', 'White5', 'Powerball']
    )

    st.subheader(f"Generated {len(combos_df)} Powerball Combinations")
    # Display table without index
    st.dataframe(
        combos_df.style.set_properties(**{'text-align': 'center'}), 
        height=400
    )

    # CSV download
    csv_data = combos_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download combinations as CSV",
        data=csv_data,
        file_name="powerball_combinations.csv",
        mime="text/csv"
    )

