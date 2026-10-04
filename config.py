
import os

# Application information
APP_NAME = "YouTube Downloader"
APP_VERSION = "1.0"

# Default download directory
DOWNLOAD_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "YouTube Downloader"
)

# Supported formats
VIDEO_FORMAT = "mp4"
AUDIO_FORMAT = "mp3"

# Create download directory
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)