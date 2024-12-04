import os

def find_iso_files(start_path):
    iso_files = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".iso"):
                iso_files.append(os.path.join(root, file))
    return iso_files

def main(drives):
    for drive in drives:
        drive_path = f"{drive}:\\"
        if not os.path.exists(drive_path):
            print(f"Drive '{drive_path}' does not exist.")
            continue

        print(f"Scanning {drive_path}")
        iso_files = find_iso_files(drive_path)
        if iso_files:
            print(f"ISO Files found on {drive_path}:")
            for iso_file in iso_files:
                print(f"ISO File: {os.path.basename(iso_file)}")
                print(f"Path: {iso_file}")
        else:
            print(f"No ISO files found on {drive_path}")

if __name__ == "__main__":
    # Example list of drive letters to scan
    drives_to_scan = ["H", "D", "E", "F", "I"]  # Add more drive letters as needed
    main(drives_to_scan)
