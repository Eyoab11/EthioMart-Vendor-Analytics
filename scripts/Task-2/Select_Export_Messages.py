# In a new Colab cell

# Reload the preprocessed data if needed
PREPROCESSED_CSV = os.path.join(GDRIVE_PROJECT_PATH, 'preprocessed_telegram_data.csv')
df = pd.read_csv(PREPROCESSED_CSV)

# Make sure we only sample from rows that have cleaned text
df_to_label = df.dropna(subset=['cleaned_text'])

# Select 50 random samples
# random_state ensures you get the same "random" sample every time you run it.
sample_messages = df_to_label['cleaned_text'].sample(n=50, random_state=42)

# Save these messages to a text file in your Drive
MESSAGES_TO_LABEL_FILE = os.path.join(GDRIVE_PROJECT_PATH, 'messages_to_label.txt')
with open(MESSAGES_TO_LABEL_FILE, 'w', encoding='utf-8') as f:
    for message in sample_messages:
        f.write(message + '\n')

print(f"✅ Successfully exported 50 sample messages to '{MESSAGES_TO_LABEL_FILE}'")
