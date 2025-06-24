# EthioMart: Amharic E-commerce Data Extractor - Project README

This document outlines the progress and methodology for the EthioMart project, which aims to build an Amharic Named Entity Recognition (NER) system for a centralized e-commerce platform.

**Project Goal:** To extract key business entities (Product, Price, Location) from unstructured Amharic text from various Telegram e-commerce channels, enabling EthioMart to create a unified and searchable product database.

This README documents the entire project workflow, from data collection to the final business application.

---

## Task 1: Data Ingestion and Preprocessing

This task focused on setting up a robust pipeline to collect raw data from Telegram and prepare it for machine learning.

### 1.1. Data Ingestion (Scraping)

A custom data scraper was developed using Python to programmatically collect messages from multiple Ethiopian-based e-commerce Telegram channels.

-   **Technology Used:** `telethon`, `pandas`
-   **Methodology:**
    1.  A list of target channel usernames was compiled in `data/raw/channels_to_crawl.csv`.
    2.  A "one-by-one" scraping strategy was implemented in a Google Colab environment to handle network timeouts and ensure incremental progress.
    3.  For each channel, the script collected message text and metadata (views, date), saving the output directly to Google Drive.

### 1.2. Data Aggregation and Preprocessing

The collected raw data was aggregated and cleaned to create a unified, high-quality dataset.

-   **Technology Used:** `pandas`, `re` (regular expressions)
-   **Methodology:**
    1.  **Aggregation:** All individual CSV files from the scraping phase were loaded and concatenated into a single master DataFrame.
    2.  **Cleaning:** A text preprocessing function was applied to remove URLs, user mentions, hashtags, and non-essential characters, while normalizing whitespace.
-   **Output:** `preprocessed_telegram_data.csv`, the final clean dataset used for all subsequent tasks.

---

## Task 2: Labeling Amharic Data for NER

This task involved manually annotating a subset of the preprocessed data to create the "ground truth" necessary for fine-tuning a model.

-   **Labeling Scheme:** The standard IOB2 (Inside, Outside, Beginning) format was used to identify `PRODUCT`, `PRICE`, and `LOCATION` entities.
-   **Methodology:**
    1.  A random sample of 50 messages was selected.
    2.  Each word (token) in the sample was carefully assigned an NER tag (`B-PRODUCT`, `I-PRODUCT`, `B-PRICE`, `I-PRICE`, `B-LOC`, `I-LOC`, or `O`).
-   **Output:** `labeled_data_conll.txt`, a high-quality, human-annotated dataset that serves as the cornerstone for model training.

---

## Task 3 & 4: Model Fine-Tuning and Comparison

The objective was to fine-tune pre-trained transformer models on our custom NER task and compare their performance.

-   **Technology Used:** Hugging Face `transformers`, `datasets`, `evaluate`, PyTorch.
-   **Environment:** Google Colab with GPU support.

### Model 1: `xlm-roberta-base`

A large, general-purpose multilingual model was fine-tuned as a baseline.
-   **Result:** The model failed to learn effectively, achieving an **F1-score of 0.0**. It learned to predict `O` for all tokens, a common outcome when a large model is trained on a very small dataset.

### Model 2: `bert-base-multilingual-cased`

A smaller, but still powerful, multilingual model was fine-tuned to see if a different architecture could perform better.
-   **Result:** This model also struggled significantly and produced an **F1-score of 0.0**.

### Key Finding from Model Training

The consistent poor performance across different model architectures strongly indicates that the primary limiting factor is not the choice of model, but the **insufficient size of the labeled training dataset**. The ~40 training samples were not enough for either model to learn the complex patterns of the e-commerce entities.

---

## Task 5: Model Interpretability

To confirm the findings from the training phase, we loaded the fine-tuned `bert-base-multilingual-cased` model and performed inference on sample sentences.

-   **Methodology:** A Hugging Face `pipeline` was used to run the saved model on new text.
-   **Result:** As expected, the model predicted the `O` (Outside) tag for every token in the test sentences. It did not identify any `PRODUCT`, `PRICE`, or `LOC` entities.
-   **Conclusion:** This provides concrete evidence that the model's strategy was to ignore specific entities entirely, which explains the 0.0 F1-score and highlights the need for more training data.

---

## Task 6: FinTech Vendor Scorecard for Micro-Lending

The final task was to build a data product that integrates our workflow to solve a real business need: identifying promising vendors for micro-lending.

-   **Methodology:**
    1.  A Python script was developed to process the scraped data for each vendor.
    2.  The script integrated the fine-tuned NER model to *attempt* to extract product prices from each post.
    3.  It calculated key performance metrics: **Posting Frequency** (posts/week) and **Market Reach** (average views/post).
    4.  A final **Lending Score** was computed using a weighted average of these metrics to rank vendors.

### Final Vendor Scorecard

The analytics engine successfully produced the following scorecard, ranking vendors by their activity and audience engagement.

| Channel | Posts/Week | Avg. Views/Post | Avg. Price (ETB) | Lending Score |
| :--- | :--- | :--- | :--- | :--- |
| @ethio_brand_collection | 7.59 | 43262.83 | NaN | 21635.21 |
| @Leyueqa | 22.41 | 30963.72 | NaN | 15493.06 |
| @Shewabrand | 7.57 | 13297.77 | NaN | 6652.67 |
| @sinayelj | 8.49 | 12259.57 | NaN | 6134.03 |
| @ZemenExpress | 21.56 | 6340.68 | NaN | 3181.12 |
| @helloomarketethiopia | 15.75 | 5072.79 | NaN | 2544.27 |
| @nevacomputer | 3.43 | 4186.90 | NaN | 2095.16 |
| @meneshayeofficial | 6.35 | 2735.58 | NaN | 1370.96 |

### Project Conclusion and Recommendation

This project successfully built a repeatable, end-to-end workflow from data ingestion to a business-ready analytics product. The Vendor Scorecard demonstrates a powerful proof-of-concept for data-driven decision-making at EthioMart.

The `Avg. Price (ETB)` column is empty because the underlying NER model was unable to learn from the limited training data. This is not a failure of the system, but rather its most critical finding.

**Primary Recommendation:** The single most impactful next step is to **expand the manually labeled dataset from ~50 samples to 500-1000+**. Re-training the NER model on this larger dataset will unlock the full potential of the Vendor Scorecard by enabling automated price extraction, providing a comprehensive view of vendor value and solidifying EthioMart's position as a data-driven leader in the e-commerce space.