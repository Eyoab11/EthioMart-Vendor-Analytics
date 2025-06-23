# In the same Colab cell, or a new one

import re

# Drop rows where the message text is empty, as they are not useful
df.dropna(subset=['Message Text'], inplace=True)
df.reset_index(drop=True, inplace=True)

def preprocess_amharic_text(text):
    """
    Cleans Amharic text by removing URLs, user mentions, hashtags,
    non-Amharic/Latin/numeric characters, and extra whitespace.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user @mentions
    text = re.sub(r'\@\w+', '', text)
    # Remove #hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove characters that are not Amharic, Latin, numbers, or basic punctuation
    # This keeps Amharic (U+1200-U+137F), basic Latin, numbers, and some punctuation.
    text = re.sub(r'[^\u1200-\u137F\s\w.,!?-]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Apply the cleaning function to the 'Message Text' column
df['cleaned_text'] = df['Message Text'].apply(preprocess_amharic_text)

print("✅ Text preprocessing complete.")
print("\n--- Comparing original vs. cleaned text ---")

# Display a sample to see the effect of cleaning
display(df[['Message Text', 'cleaned_text']].head(10))

# Save the final preprocessed data
PREPROCESSED_CSV = os.path.join(GDRIVE_PROJECT_PATH, 'preprocessed_telegram_data.csv')
df.to_csv(PREPROCESSED_CSV, index=False)
print(f"\nSaved the final preprocessed data to: {PREPROCESSED_CSV}")