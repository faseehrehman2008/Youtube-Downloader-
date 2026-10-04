
import yt_dlp
import os


class Downloader:

    def __init__(self, download_path):

        self.download_path = download_path

    def download(self, url, quality, file_format, progress_callback=None):

        if not os.path.isdir(self.download_path):
            raise FileNotFoundError("Download folder does not exist.")

        if file_format == "MP3 Audio":

            options = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(
                    self.download_path,
                    "%(title)s.%(ext)s"
                ),
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            }

        else:

            quality_map = {
                "Best Available": "bestvideo+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "480p": "bestvideo[height<=480]+bestaudio/best",
                "360p": "bestvideo[height<=360]+bestaudio/best"
            }

            options = {
                "format": quality_map.get(
                    quality,
                    "bestvideo+bestaudio/best"
                ),
                "merge_output_format": "mp4",
                "outtmpl": os.path.join(
                    self.download_path,
                    "%(title)s.%(ext)s"
                ),
                "noplaylist": True
            }

        if progress_callback:

            def progress_hook(data):

                if data["status"] == "downloading":

                    total = data.get("total_bytes") or data.get(
                        "total_bytes_estimate"
                    )

                    if total:
                        percentage = data.get("downloaded_bytes", 0) / total
                        progress_callback(percentage)

                elif data["status"] == "finished":
                    progress_callback(1.0)

            options["progress_hooks"] = [progress_hook]

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])