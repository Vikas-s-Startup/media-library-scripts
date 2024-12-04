import os
import string
from ctypes import windll


def get_drives():
    """Returns a list of all available drive letters on Windows, excluding C: and G:."""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1

    # Exclude specific drives
    excluded_drives = ["C:\\", "G:\\"]
    drives = [drive for drive in drives if drive not in excluded_drives]

    return drives


def human_readable_size(size):
    """Converts file size from bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"  # For exceptionally large files


def search_files(drives, keywords):
    """Searches for files containing specific keywords in their names across drives and prints their sizes."""
    for drive in drives:
        for root, _, files in os.walk(drive):
            for file in files:
                if any(keyword in file for keyword in keywords):
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)  # Get file size in bytes
                        print(f"Found: {file} in {root} - Size: {human_readable_size(file_size)}")
                    except (OSError, FileNotFoundError):
                        print(f"Error accessing file: {file_path}")


def search_folders_with_indian(drives):
    """Searches for folders with 'Indian' in their names across drives."""
    indian_folders = []
    for drive in drives:
        for root, dirs, _ in os.walk(drive):
            for directory in dirs:
                if "Indian" in directory:  # Case-sensitive match; for case-insensitive use `.lower()`:
                    indian_folders.append(os.path.join(root, directory))
    return indian_folders


if __name__ == "__main__":
    # Keywords to search for in file names
    keywords = ["-DTR", "-JATT", "-Telly", "-DTLegacy", "-Banana"]

    # Get all drives
    drives = get_drives()

    # Print all drives
    print(f"Drives found: {drives}")

    # Search and print folders with "Indian" in the name
    indian_folders = search_folders_with_indian(drives)
    print("\nFolders with 'Indian' in their names:")
    for folder in indian_folders:
        print(folder)

    # Search files containing specific keywords and print file sizes
    print("\nSearching for files with specified keywords and their sizes:")
    search_files(drives, keywords)
