from plexapi.server import PlexServer
import os
import send2trash


# Your Plex server URL and Plex token
plex_url = 'http://127.0.0.1:32400'
plex_token = 'ur66esayPiZCUT4vnjq2'
plex = PlexServer(plex_url, plex_token)

# Select your movie library
indian_movies = plex.library.section('International')

duplicates = indian_movies.search(duplicate=True)


def get_file_size(path):
    try:
        size_bytes = os.path.getsize(path)
        size_mb = size_bytes / (1024 * 1024)
        if size_mb > 1024:
            return f"{size_mb / 1024:.2f} GB"
        else:
            return f"{size_mb:.2f} MB"
    except FileNotFoundError:
        return "0 MB"


for duplicate in duplicates:
    print("\nDuplicate Movie: ", duplicate.title)
    file_locations = duplicate.locations
    for index, dp_location in enumerate(file_locations):
        print(f"{index}. Size: {get_file_size(dp_location)} Found at: {dp_location}")

    print("Select an option:")
    print("1 - Delete a specific file")
    print("2 - Delete all except one")
    print("3 - Skip to next movie")
    choice = input("Enter your choice: ")

    if choice == '1':
        file_index = int(input("Enter the index of the file to delete: "))
        os.remove(file_locations[file_index])
        print("File deleted.")
    elif choice == '2':
        keep_index = int(input("Enter the index of the file to keep: "))
        for i, location in enumerate(file_locations):
            if i != keep_index:
                # os.remove(location)
                try:
                    send2trash.send2trash(location)
                except Exception as e:
                    print(f"Error: {e}")
                print(f"Deleted: {location}")
        print("All duplicates deleted except the chosen file.")
    elif choice == '3':
        print("Skipping to next movie.")
    else:
        print("Invalid choice. Skipping to next movie.")
    print("\n----------------------------------------\n")
