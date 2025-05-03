import os
import subprocess
import tempfile
from send2trash import send2trash  # Safer file deletion

# Keywords to search for in filenames
KEYWORDS = ["pre-hd", "real", "predvd", "hdts"]


def get_friendly_path(path):
    return os.path.abspath(os.path.normpath(os.path.expanduser(path)))


def find_matching_files(drive_paths):
    matched_files = []

    for drive in drive_paths:
        friendly_path = get_friendly_path(drive)
        for root, dirs, files in os.walk(friendly_path):
            for file in files:
                filename_lower = file.lower()
                if any(keyword in filename_lower for keyword in KEYWORDS):
                    full_path = os.path.join(root, file)
                    matched_files.append(full_path)

    if matched_files:
        print("\n🔍 Matching files found:")
        for path in matched_files:
            print(path)
    else:
        print("\n✅ No matching files found in the specified paths.")

    return matched_files


def create_m3u_playlist(file_paths):
    playlist_path = os.path.join(tempfile.gettempdir(), "filtered_playlist.m3u")
    with open(playlist_path, 'w', encoding='utf-8') as f:
        for path in file_paths:
            f.write(path + '\n')
    return playlist_path


def open_in_vlc_with_playlist(file_paths):
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    m3u_path = create_m3u_playlist(file_paths)

    try:
        subprocess.Popen([vlc_path, m3u_path])
        print(f"\n✅ Opened VLC with playlist: {m3u_path}")
    except Exception as e:
        print(f"❌ Failed to open VLC. Error: {e}")


def move_files_to_trash(file_paths):
    print("\n⚠️ Moving files to Recycle Bin...")
    for path in file_paths:
        try:
            send2trash(path)
            print(f"🗑️ Moved to Recycle Bin: {path}")
        except Exception as e:
            print(f"❌ Failed to move {path} to trash: {e}")
    print("\n✅ All selected files moved to Recycle Bin.")


# Example usage
drive_locations = [
    r"D:\Movies\Indian",
    r"E:\Movies\Indian",
    r"F:\Movies\Indian",
    r"H:\Indian",
    r"I:\Indian",
    r"J:\Movies\Indian",
    r"L:\Movies\Indian"
]

matched_files = find_matching_files(drive_locations)

if matched_files:
    print("\nWhat do you want to do with these files?")
    print("1. Move to Recycle Bin")
    print("2. Play in VLC")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        move_files_to_trash(matched_files)
    elif choice == '2':
        open_in_vlc_with_playlist(matched_files)
    else:
        print("❌ Invalid choice. No action taken.")
