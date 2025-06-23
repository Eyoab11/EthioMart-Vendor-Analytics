# In a new Colab cell

import pandas as pd
import glob
import os

# This should be the same path you used in your scraper setup
GDRIVE_PROJECT_PATH = '/content/drive/MyDrive/Ethio_mart' 
SCRAPED_DATA_PATH = os.path.join(GDRIVE_PROJECT_PATH, 'scraped_data')

# Use glob to find all the CSV files you created
all_csv_files = glob.glob(os.path.join(SCRAPED_DATA_PATH, '*/*_data.csv'))

if not all_csv_files:
    print("❌ ERROR: No CSV files found. Make sure your path is correct and you have scraped the data.")
else:
    print(f"Found {len(all_csv_files)} CSV files to merge.")
    print("Files found:", all_csv_files)

    # Read and combine all files into a single DataFrame
    li = []
    for filename in all_csv_files:
        df_single = pd.read_csv(filename, index_col=None, header=0)
        li.append(df_single)

    df = pd.concat(li, axis=0, ignore_index=True)

    print("\n✅ All data successfully combined!")
    print("\n--- Combined DataFrame Info ---")
    df.info()

    print("\n--- First 5 Rows of Combined Data ---")
    display(df.head())

    # Save the combined, raw data for backup
    COMBINED_RAW_CSV = os.path.join(GDRIVE_PROJECT_PATH, 'combined_telegram_data_raw.csv')
    df.to_csv(COMBINED_RAW_CSV, index=False)
    print(f"\nSaved the combined raw data to: {COMBINED_RAW_CSV}")