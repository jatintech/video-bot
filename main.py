import os
import asyncio
import requests
import aiohttp
from tqdm import tqdm

BASE_URL = "https://api.socialverseapp.com/posts"
FLIC_TOKEN = "flic_93f25f0172a924a3019af08ad2f761b89ef318767719a1ff7ddb0c055872ee8b" 
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json"
}
VIDEOS_DIR = "./videos"

async def fetch_upload_url(session):
    """Fetch pre-signed upload URL."""
    async with session.get(f"{BASE_URL}/generate-upload-url", headers=HEADERS) as response:
        if response.status == 200:
            response_json = await response.json()
            print("API Response:", response_json)  
            return response_json
        else:
            raise Exception(f"Failed to fetch upload URL: {response.status}")


async def upload_video(file_path, upload_url):
    """Upload video using pre-signed URL."""
    with open(file_path, 'rb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.put(upload_url, data=f) as response:
                if response.status != 200:
                    raise Exception(f"Failed to upload video: {response.status}")

async def create_post(session, title, video_hash, category_id):
    """Create a new post."""
    data = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": True,
        "category_id": category_id
    }
    async with session.post(BASE_URL, headers=HEADERS, json=data) as response:
        if response.status == 200:
            return await response.json()
        else:
            error_message = await response.text()
            raise Exception(f"Failed to create post: {response.status}, Response: {error_message}")

async def process_video(file_path, title, category_id):
    """Handle video upload and post creation."""
    async with aiohttp.ClientSession() as session:
        print(f"Processing {file_path}...")

        # Fetch the pre-signed upload URL from the API
        upload_info = await fetch_upload_url(session)
        
        # Ensure that the required data ('url' and 'hash') is in the API response
        if 'url' not in upload_info or 'hash' not in upload_info:
            raise Exception("Failed to get 'url' or 'hash' from API response")

        # Extract the upload URL and video hash from the API response
        upload_url = upload_info['url']  
        video_hash = upload_info['hash']

        # Upload the video file to the pre-signed URL
        await upload_video(file_path, upload_url)

        # Create a post with the uploaded video
        await create_post(session, title, video_hash, category_id)

        # After processing the video, remove it from the local filesystem
        os.remove(file_path)
        print(f"Finished processing {file_path} and deleted it locally.")



async def monitor_directory():
    """Monitor the videos directory for new .mp4 files."""
    print("Monitoring /videos for new files...")
    processed_files = set()

    while True:
        for file_name in os.listdir(VIDEOS_DIR):
            if file_name.endswith(".mp4") and file_name not in processed_files:
                file_path = os.path.join(VIDEOS_DIR, file_name)
                processed_files.add(file_name)
                await process_video(file_path, title="Sample Title", category_id=1)
        await asyncio.sleep(5)

if __name__ == "__main__":
    if not os.path.exists(VIDEOS_DIR):
        os.makedirs(VIDEOS_DIR)

    asyncio.run(monitor_directory())
