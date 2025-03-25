import os
import re


def remove_extra_after_flac(directory):
    """Removes everything after '.flac' in filenames, handling duplicates."""
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        if not os.path.isfile(old_path):
            continue

        # Keep only the part before and including '.flac'
        match = re.match(r'(.+?\.flac)', filename)
        if match:
            new_filename = match.group(1)
            new_path = os.path.join(directory, new_filename)

            # Handle duplicate filenames by appending a counter
            counter = 1
            while os.path.exists(new_path):
                base_name, extension = os.path.splitext(new_filename)
                new_filename = f"{base_name}_{counter}{extension}"
                new_path = os.path.join(directory, new_filename)
                counter += 1

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    folder_path = r"M:\TIDAL\all_songs_i_like_tidal_transfer_playlist_6"
    remove_extra_after_flac(folder_path)