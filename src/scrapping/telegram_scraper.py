import os
import csv
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChannelPrivateError, ChannelInvalidError

# --- Configuration ---

# Load environment variables from the root directory of the project
# This path is relative to this script's location (src/scraping/)
load_dotenv('../../.env') 
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Set the limit of messages to scrape per channel. Set to None to attempt to scrape all messages.
MESSAGE_LIMIT = 2000 

# Define input and output paths based on the project structure
# These paths are relative to this script's location.
RAW_DATA_DIR = '../../data/raw'
MEDIA_DIR = os.path.join(RAW_DATA_DIR, 'media')
CHANNEL_LIST_PATH = '../../data/raw/channels_to_crawl.csv' # Your CSV file with channel names
OUTPUT_CSV_PATH = os.path.join(RAW_DATA_DIR, 'telegram_data_raw.csv')


async def scrape_channel(client, channel_username, writer):
    """
    Scrapes messages from a single Telegram channel and writes them to a CSV file.
    Also downloads associated media.
    """
    try:
        print(f"--- Starting scrape for {channel_username} ---")
        entity = await client.get_entity(channel_username)
        channel_title = getattr(entity, 'title', 'N/A')

        async for message in client.iter_messages(entity, limit=MESSAGE_LIMIT):
            # Skip messages that have no text and no media
            if not message.message and not message.media:
                continue

            media_path = None
            # Check for photo or video media and attempt to download
            if message.media:
                # Create a unique filename base for the media
                filename_base = f"{channel_username.replace('@', '')}_{message.id}"
                media_file_path = os.path.join(MEDIA_DIR, filename_base)
                
                try:
                    # Telethon automatically adds the correct file extension
                    downloaded_path = await client.download_media(message.media, file=media_file_path)
                    # Use the relative path for the CSV file
                    media_path = os.path.relpath(downloaded_path, os.path.dirname(OUTPUT_CSV_PATH))
                except Exception as e:
                    print(f"Could not download media for message {message.id} from {channel_username}: {e}")
                    media_path = "download_failed"

            # Write the row to the CSV file
            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                message.date,
                message.message,
                message.views, # Crucial metric for Task 6
                media_path
            ])
        print(f"--- Finished scraping for {channel_username}. Processed messages. ---")

    except (ChannelPrivateError, ChannelInvalidError):
        print(f"Error: Could not access channel '{channel_username}'. It may be private or the username is incorrect. Skipping.")
    except ValueError:
        print(f"Error: Channel username '{channel_username}' could not be found. Skipping.")
    except Exception as e:
        print(f"An unexpected error occurred for channel {channel_username}: {e}")


async def main():
    """
    Main function to initialize the client and orchestrate the scraping process.
    """
    # Initialize the client. The session file will be created in the same directory as the script.
    client = TelegramClient('scraping_session', api_id, api_hash)
    
    await client.start(phone)
    print("Telegram client started successfully.")

    # Create necessary directories if they don't exist
    os.makedirs(MEDIA_DIR, exist_ok=True)

    # Read the list of channels from the specified CSV file
    try:
        with open(CHANNEL_LIST_PATH, 'r', encoding='utf-8') as f:
            # Create a list of channels, stripping whitespace. Ignores empty lines.
            channels = [line.strip() for line in f if line.strip()]
        if not channels:
            print(f"Error: '{CHANNEL_LIST_PATH}' is empty. Please add channel usernames.")
            return
        print(f"Found {len(channels)} channels to scrape from '{CHANNEL_LIST_PATH}'.")
    except FileNotFoundError:
        print(f"Error: Channel list file '{CHANNEL_LIST_PATH}' not found. Please create it in the 'src/scraping' directory.")
        return

    # Open the single CSV file to write all data
    with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Channel Title', 'Channel Username', 'Message ID', 'Date', 'Message Text', 'Views', 'Media Path'])
        
        # Iterate over channels and scrape data into the single CSV
        for channel in channels:
            await scrape_channel(client, channel, writer)
            
    print(f"\nScraping complete. All data saved to '{OUTPUT_CSV_PATH}'")
    await client.disconnect()
    print("Client disconnected.")


if __name__ == "__main__":
    # Use asyncio.run() to execute the main asynchronous function
    asyncio.run(main())