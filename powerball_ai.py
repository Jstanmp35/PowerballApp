import pandas as pd
import random
import csv

# --- Safe CSV loader with auto-detect for white ball columns ---
def load_data(file_path="powerball_all.csv"):
    """
    Load Powerball historical data safely.
    Auto-detects CSV delimiter, handles BOM and extra spaces.
    Returns DataFrame and the detected white ball columns.
    """
    # Auto-detect delimiter
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        sample = f.read(1024)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        delimiter = dialect.delimiter

    df = pd.read_csv(file_path, encoding='utf-8-sig', sep=delimiter)
    df.columns = df.columns.str.strip()  # remove spaces

    # Auto-detect white ball columns (must have 5)
    white_cols = [c for c in df.columns if 'Bal' in c or 'Ball' in c][:5]
    if len(white_cols) != 5:
        raise ValueError(f"Could not find exactly 5 white ball columns, found: {white_cols}")

    return df, white_cols

# --- Generate top combinations ---
def generate_top_combos(num_combos=10):
    """
    Generate a list of unique Powerball combinations:
    - 5 white balls (1-69)
    - 1 Powerball (1-26)
    """
    combos = []
    while len(combos) < num_combos:
        white_balls = sorted(random.sample(range(1, 70), 5))
        powerball = random.randint(1, 26)
        combo = (*white_balls, powerball)
        if combo not in combos:
            combos.append(combo)
    return combos

# --- Optional: Analyze historical patterns ---
def most_common_numbers(df, white_cols, top_n=5):
    """
    Return the most common white balls in historical draws.
    """
    all_white_balls = df[white_cols].values.flatten()
    counts = pd.Series(all_white_balls).value_counts()
    return counts.head(top_n)

# --- Test run ---
if __name__ == "__main__":
    df, white_cols = load_data()
    print(f"Loaded {len(df)} past draws successfully.")

    print("\nTop 5 most common white balls historically:")
    print(most_common_numbers(df, white_cols, top_n=5))

    top_combos = generate_top_combos(10)
    print("\nGenerated Powerball combinations:")
    for combo in top_combos:
        print(combo)



