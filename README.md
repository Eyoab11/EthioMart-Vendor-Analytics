# EthioMart: Amharic E-commerce Data Extractor - Project README

This document outlines the progress and methodology for the EthioMart project, which aims to build an Amharic Named Entity Recognition (NER) system for a centralized e-commerce platform.

**Project Goal:** To extract key business entities (Product, Price, Location) from unstructured Amharic text from various Telegram e-commerce channels, enabling EthioMart to create a unified and searchable product database.

This README covers the completion of **Task 1 (Data Ingestion and Preprocessing)** and **Task 2 (Data Labeling)**.

---

## Task 1: Data Ingestion and Preprocessing

This task focused on setting up a robust pipeline to collect raw data from Telegram and prepare it for machine learning.

### 1.1. Data Ingestion (Scraping)

A custom data scraper was developed using Python to programmatically collect messages from multiple Ethiopian-based e-commerce Telegram channels.

-   **Technology Used:** `telethon` (a Python library for interacting with the Telegram API).
-   **Methodology:**
    1.  A list of target channel usernames was compiled in `data/raw/channels_to_crawl.csv`.
    2.  The scraper was configured to authenticate with the Telegram API using credentials stored securely in a `.env` file.
    3.  A "one-by-one" scraping strategy was implemented in a Google Colab environment to handle potential network timeouts and large channels gracefully. This approach isolates failures and ensures incremental progress.
    4.  For each target channel, the script iterated through recent messages, collecting message text, metadata (like views and date), and downloading associated media (images/videos).
-   **Output:**
    -   A dedicated CSV file for each scraped channel (e.g., `ZemenExpress_data.csv`), containing structured message data.
    -   A corresponding media folder for each channel, storing all downloaded images and videos.
    -   All outputs were saved directly to a persistent Google Drive folder to prevent data loss.

### 1.2. Data Aggregation and Preprocessing

Once the raw data was collected, it was aggregated and cleaned to create a unified, high-quality dataset.

-   **Technology Used:** `pandas`, `re` (for regular expressions).
-   **Methodology:**
    1.  **Aggregation:** All individual CSV files from the scraping phase were loaded and concatenated into a single master `pandas` DataFrame.
    2.  **Cleaning:** A text preprocessing function was applied to the `Message Text` column to:
        -   Remove URLs, email addresses, and Telegram user mentions (`@username`).
        -   Strip out hashtags (`#hashtag`).
        -   Eliminate special characters, emojis, and non-essential punctuation, while preserving Amharic and basic Latin characters.
        -   Normalize whitespace by removing extra spaces, tabs, and newlines.
-   **Output:**
    -   `combined_telegram_data_raw.csv`: A backup file containing the merged but uncleaned data.
    -   `preprocessed_telegram_data.csv`: The final, clean dataset with an added `cleaned_text` column, ready for the labeling phase.

---

## Task 2: Labeling Amharic Data for NER

This task involved manually annotating a subset of the preprocessed data to create the "ground truth" necessary for fine-tuning a Named Entity Recognition model.

### 2.1. Dataset Preparation for Labeling

A representative sample of the cleaned data was prepared for manual annotation.

-   **Methodology:**
    1.  A random sample of 50 messages was selected from the `cleaned_text` column of the preprocessed dataset.
    2.  These messages were exported to a plain text file (`messages_to_label.txt`) for easy access.

### 2.2. Manual Annotation in CoNLL Format

The core of this task was the careful, manual labeling of each token (word) in the sample messages.

-   **Labeling Scheme:** The standard IOB2 (Inside, Outside, Beginning) scheme was used.
    -   `B-PRODUCT`: Beginning of a product name.
    -   `I-PRODUCT`: Inside a product name.
    -   `B-PRICE`: Beginning of a price mention.
    -   `I-PRICE`: Inside a price mention.
    -   `B-LOC`: Beginning of a location name.
    -   `I-LOC`: Inside a location name.
    -   `O`: Outside any named entity.
-   **Methodology:**
    1.  Each message was tokenized (split into words).
    2.  Each token was assigned one of the predefined NER tags.
    3.  The final labeled data was structured in the **CoNLL format**, where each line contains a token followed by its corresponding tag, and sentences are separated by a blank line.
-   **Output:**
    -   `labeled_data_conll.txt`: A high-quality, manually annotated dataset containing the labeled text. This file serves as the cornerstone for training and evaluating the NER model in the subsequent tasks.

---

## Next Steps

With the completion of Tasks 1 and 2, the project is now ready for **Task 3: Fine-Tuning Existing Models for NER**. The `labeled_data_conll.txt` file will be used to adapt a pre-trained transformer model (e.g., XLM-Roberta) to accurately recognize Amharic e-commerce entities.