import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

from downloader import Downloader
from config import DOWNLOAD_FOLDER, APP_NAME, APP_VERSION


# Application settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeDownloader:

    def __init__(self, root):

        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        self.download_path = DOWNLOAD_FOLDER

        os.makedirs(self.download_path, exist_ok=True)

        self.create_widgets()

    # ===============================
    # CREATE GUI
    # ===============================

    def create_widgets(self):

        # Main heading
        title = ctk.CTkLabel(
            self.root,
            text="YouTube Downloader",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Download media you are authorized to save",
            font=("Arial", 13)
        )
        subtitle.pack(pady=(0, 25))

        # URL input
        url_label = ctk.CTkLabel(
            self.root,
            text="YouTube Video URL",
            font=("Arial", 15, "bold")
        )
        url_label.pack(anchor="w", padx=70)

        self.url_entry = ctk.CTkEntry(
            self.root,
            width=610,
            height=45,
            placeholder_text="Paste your YouTube URL here..."
        )
        self.url_entry.pack(pady=10)

        # Quality selection
        quality_label = ctk.CTkLabel(
            self.root,
            text="Select Video Quality",
            font=("Arial", 15, "bold")
        )
        quality_label.pack(anchor="w", padx=70, pady=(15, 5))

        self.quality_option = ctk.CTkOptionMenu(
            self.root,
            values=[
                "Best Available",
                "1080p",
                "720p",
                "480p",
                "360p"
            ],
            width=250,
            height=40
        )
        self.quality_option.pack(anchor="w", padx=70)

        # Format selection
        format_label = ctk.CTkLabel(
            self.root,
            text="Download Format",
            font=("Arial", 15, "bold")
        )
        format_label.pack(anchor="w", padx=70, pady=(15, 5))

        self.format_option = ctk.CTkOptionMenu(
            self.root,
            values=[
                "MP4 Video",
                "MP3 Audio"
            ],
            width=250,
            height=40
        )
        self.format_option.pack(anchor="w", padx=70)

        # Download location
        location_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        location_frame.pack(
            fill="x",
            padx=70,
            pady=20
        )

        self.location_label = ctk.CTkLabel(
            location_frame,
            text=f"Save Location: {self.download_path}",
            font=("Arial", 12),
            anchor="w"
        )
        self.location_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        browse_button = ctk.CTkButton(
            location_frame,
            text="Browse",
            width=100,
            command=self.select_folder
        )
        browse_button.pack(side="right")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.root,
            width=610,
            height=15
        )
        self.progress_bar.pack(pady=(10, 5))
        self.progress_bar.set(0)

        # Status
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Ready to download",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=5)

        # Download button
        self.download_button = ctk.CTkButton(
            self.root,
            text="Download",
            width=220,
            height=45,
            font=("Arial", 16, "bold"),
            command=self.start_download
        )
        self.download_button.pack(pady=20)

        # Footer
        footer = ctk.CTkLabel(
            self.root,
            text="Python Project | YouTube Downloader",
            font=("Arial", 11)
        )
        footer.pack(side="bottom", pady=15)

    # ===============================
    # SELECT DOWNLOAD FOLDER
    # ===============================

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=self.download_path
        )

        if folder:

            self.download_path = folder

            self.location_label.configure(
                text=f"Save Location: {folder}"
            )

    # ===============================
    # UPDATE PROGRESS
    # ===============================

    def update_progress(self, value):

        self.root.after(
            0,
            lambda: self.progress_bar.set(value)
        )

    # ===============================
    # START DOWNLOAD
    # ===============================

    def start_download(self):

        url = self.url_entry.get().strip()

        if not url:

            messagebox.showwarning(
                "Missing URL",
                "Please enter a video URL."
            )
            return

        if not url.startswith(("https://", "http://")):

            messagebox.showwarning(
                "Invalid URL",
                "Please enter a valid URL."
            )
            return

        quality = self.quality_option.get()
        file_format = self.format_option.get()

        downloader = Downloader(self.download_path)

        # Reset progress
        self.progress_bar.set(0)

        self.status_label.configure(
            text="Preparing download..."
        )

        self.download_button.configure(
            state="disabled",
            text="Downloading..."
        )

        # Background download thread
        def download_task():

            try:

                downloader.download(
                    url=url,
                    quality=quality,
                    file_format=file_format,
                    progress_callback=self.update_progress
                )

                self.root.after(
                    0,
                    self.download_success
                )

            except Exception as error:

                self.root.after(
                    0,
                    lambda err=str(error): self.download_error(err)
                )

        threading.Thread(
            target=download_task,
            daemon=True
        ).start()

    # ===============================
    # DOWNLOAD SUCCESS
    # ===============================

    def download_success(self):

        self.progress_bar.set(1)

        self.status_label.configure(
            text="Download completed successfully!"
        )

        self.download_button.configure(
            state="normal",
            text="Download"
        )

        messagebox.showinfo(
            "Success",
            f"Your file has been saved in:\n\n{self.download_path}"
        )

    # ===============================
    # DOWNLOAD ERROR
    # ===============================

    def download_error(self, error):

        self.status_label.configure(
            text="Download failed!"
        )

        self.download_button.configure(
            state="normal",
            text="Download"
        )

        messagebox.showerror(
            "Download Error",
            error
        )


# ===============================
# RUN APPLICATION
# ===============================

if __name__ == "__main__":

    root = ctk.CTk()

    app = YouTubeDownloader(root)

    root.mainloop()