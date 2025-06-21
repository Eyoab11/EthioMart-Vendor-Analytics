import re
import pandas as pd
import os

def clean_telegram_message(text):
    """
    Cleans a single Telegram message text by removing URLs, emojis,
    special characters, and normalizing whitespace.
    """
    if not isinstance(text, str):
        return "" # Return empty string for non-text data (like NaN)

    # 1. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 2. Remove Telegram usernames and channel links
    text = re.sub(r'@\w+', '', text)
    
    # 3. Remove Emojis (this is a basic regex, more comprehensive ones exist)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub(r'', text)

    # 4. Remove other special characters but keep Amharic and basic punctuation
    # Keeps letters, numbers, and some punctuation relevant for context.
    text = re.sub(r'[^\w\s\d\.-፡።፣፤፥፦]', '', text)

    # 5. Normalize whitespace: replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_data(raw_csv_path, preprocessed_csv_path):
    """
    Reads raw scraped data, cleans the message text, and saves it.
    """
    print(f"Reading raw data from {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)

    print("Cleaning 'Message Text' column...")
    # Apply the cleaning function
    df['cleaned_text'] = df['Message Text'].apply(clean_telegram_message)

    # Filter out rows where the cleaned text is empty
    df = df[df['cleaned_text'] != ''].copy()

    # Select and save relevant columns
    output_df = df[['Channel Title', 'Channel Username', 'cleaned_text']]
    output_df.to_csv(preprocessed_csv_path, index=False, encoding='utf-8')
    print(f"Preprocessing complete. Cleaned data saved to {preprocessed_csv_path}")


if __name__ == '__main__':
    RAW_DATA_PATH = '../../data/raw/telegram_data_raw.csv'
    PREPROCESSED_PATH = '../../data/preprocessed/cleaned_messages.csv'
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(PREPROCESSED_PATH), exist_ok=True)
    
    preprocess_data(RAW_DATA_PATH, PREPROCESSED_PATH)