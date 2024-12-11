# Video Bot

## Overview

The **Video Bot** is a Python-based automation script designed to monitor a local directory (`/videos`) for new `.mp4` video files. Upon detecting a new file, the bot automatically uploads it to a video-sharing platform via the SocialVerse API, and creates a post associated with the video. The bot ensures that the video file is deleted locally once the upload and post creation are successful.

This is ideal for automating video uploads to a platform while maintaining a clean local storage system.

## Features

- **Directory Monitoring**: Continuously checks the `/videos` directory for new `.mp4` files.
- **Asynchronous Operations**: Utilizes `asyncio` and `aiohttp` to ensure efficient, non-blocking HTTP requests.
- **Video Uploading**: Uses a pre-signed URL from the SocialVerse API to securely upload video files.
- **Post Creation**: Automatically creates a post on the platform with the uploaded video, associating it with a given category.
- **Local File Cleanup**: After processing, the bot deletes the video file locally to save space.

## Requirements

- Python 3.7 or higher
- Access to the SocialVerse API (requires an API token)

## Installation

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/video-bot.git
cd video-bot
