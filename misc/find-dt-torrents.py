import json
import os
import shutil

# Define paths
json_file_path = r"C:\Users\vikaskoppineedi\Desktop\torrents_info.json"
downloads_folder = r"C:\Users\vikaskoppineedi\Downloads\dt"  # Change this if needed
destination_root = os.path.join(downloads_folder, "Sorted_Torrents")  # Parent folder for sorted torrents

# Read the JSON file
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Create a dictionary to track counts
count_dict = {drive: 0 for drive in "DEFGHIJ"}

# Process each torrent entry
for block in data:
    if "desitorrents" in block["torrentsTags"]:
        torrent_name = block["torrentFileName"]
        torrent_save_location = block["torrentSaveLocation"]

        # Determine the drive (D, E, F, etc.)
        drive_letter = torrent_save_location[0]  # Extract first letter (drive)

        # Ensure it's a valid drive
        if drive_letter in count_dict:
            source_file = os.path.join(downloads_folder, torrent_name)
            destination_folder = os.path.join(destination_root, drive_letter)  # Destination folder

            # Check if the torrent file exists in Downloads
            if os.path.exists(source_file):
                # Create the destination folder if it doesn't exist
                os.makedirs(destination_folder, exist_ok=True)

                # Move the file
                shutil.move(source_file, os.path.join(destination_folder, os.path.basename(source_file)))
                print(f"Moved: {torrent_name} to {destination_folder}")

                # Increment count
                count_dict[drive_letter] += 1

# Print summary
for drive, count in count_dict.items():
    print(f"Torrents moved to {drive}: {count}")
