from plexapi.server import PlexServer

# Replace with your Plex server details
PLEX_URL = "http://127.0.0.1:32400"
PLEX_TOKEN = "local-213cb42c-cd00-466c-9ddc-b2b2432bdc43"


def list_plex_libraries():
    try:
        plex = PlexServer(PLEX_URL, PLEX_TOKEN)
        print(f"Connected to Plex Server: {plex.friendlyName}\n")

        libraries = plex.library.sections()
        for library in libraries:
            print(f"Library: {library.title} (Type: {library.type})")
            if hasattr(library, 'locations'):
                for folder in library.locations:
                    print(f"  - Folder: {folder}")
            else:
                print("  - No folders found")
            print("-" * 40)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    list_plex_libraries()
