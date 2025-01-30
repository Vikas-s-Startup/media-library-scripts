import os

# Define the folder path
folder_path = r"C:\Users\vikaskoppineedi\Downloads\dt"  # Use raw string (r"") to handle backslashes

# Define the prefix to remove
prefix = "[DesiTorrents][88894654]"

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.startswith(prefix):
        new_name = filename[len(prefix):].lstrip()  # Remove prefix and leading spaces
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f'Renamed: "{filename}" -> "{new_name}"')

print("Renaming complete.")
