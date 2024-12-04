import os

def search_for_bdmv_folders(drive_letters):
    for letter in drive_letters:
        drive = f"{letter.upper()}:/"
        if not os.path.exists(drive):
            print(f"Drive {drive} does not exist.")
            continue

        print(f"Searching in drive {drive}:")
        for root, dirs, files in os.walk(drive):
            for folder in dirs:
                if folder.upper() == "BDMV":
                    print(os.path.join(root, folder))

# Example usage:
drives_to_scan = ["H", "D", "E", "F", "I"]
search_for_bdmv_folders(drives_to_scan)
