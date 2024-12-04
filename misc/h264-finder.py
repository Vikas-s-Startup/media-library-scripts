import os
import subprocess
from pathlib import Path

def is_h264(file_path):
    """Check if the video file is H.264 encoded using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=nw=1:nk=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip() == 'h264'
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return False

def scan_drive(drive):
    """Recursively scan the drive for video files and check if they are H.264 encoded."""
    drive_path = Path(drive)
    if not drive_path.exists():
        print(f"Drive {drive} does not exist.")
        return

    for file_path in drive_path.rglob('*'):
        if file_path.suffix.lower() in ['.mkv', '.mp4']:
            if is_h264(file_path):
                print(f"File '{file_path}' is H.264 encoded.")

def main():
    drives = input("Enter the drive letters to scan (e.g., E D F G): ").split()
    for drive in drives:
        scan_drive(drive + ':/')

if __name__ == "__main__":
    main()
