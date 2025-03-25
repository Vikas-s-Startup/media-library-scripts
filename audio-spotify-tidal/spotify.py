import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials (ensure these are set in environment variables)
SPOTIPY_CLIENT_ID = "38bf43e782204a0ddd195d0bb036a8a73ee"
SPOTIPY_CLIENT_SECRET = "dd4777f6c2bddddb49b0a9f18cf6e2e0a42a"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-library-read playlist-modify-public playlist-modify-private"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# Get current user ID
user_id = sp.current_user()["id"]


# Function to fetch all liked songs
def get_liked_songs():
    liked_tracks = []
    results = sp.current_user_saved_tracks(limit=50)

    while results:
        for item in results["items"]:
            liked_tracks.append(item["track"]["id"])

        if results["next"]:
            results = sp.next(results)
        else:
            break

    return liked_tracks


# Function to split list into chunks of `size`
def chunkify(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


# Function to add tracks in batches of 100
def add_tracks_in_batches(playlist_id, track_list):
    track_batches = chunkify(track_list, 100)
    for batch in track_batches:
        sp.playlist_add_items(playlist_id=playlist_id, items=batch)


# Fetch all liked songs
liked_songs = get_liked_songs()
print(f"✅ Fetched {len(liked_songs)} liked songs.")

# Split into chunks of 300 songs
track_chunks = chunkify(liked_songs, 300)

# Create playlists and add songs
for i, chunk in enumerate(track_chunks):
    playlist_name = f"liked_songs_tidal_transfer_playlist_{i + 1}"

    # Create playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist["id"]

    # Add tracks in batches of 100
    add_tracks_in_batches(playlist_id, chunk)

    print(f"✅ Created {playlist_name} with {len(chunk)} tracks.")

print("🎵 All playlists created successfully!")


# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Spotify credentials (ensure these are set in environment variables)
# SPOTIPY_CLIENT_ID = "38bf43e782204a0195d0bb0sss36a8a73ee"
# SPOTIPY_CLIENT_SECRET = "dd4777f6c2bb49b0a9fssss18cf6e2e0a42a"
# SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
# SCOPE = "playlist-read-private playlist-modify-public playlist-modify-private"
#
# # Authenticate with Spotify
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                scope=SCOPE))
#
# # Get current user ID
# user_id = sp.current_user()["id"]
#
#
# # Function to fetch all songs from a given playlist (SKIP None Tracks)
# def get_playlist_tracks(playlist_id):
#     tracks = []
#     results = sp.playlist_tracks(playlist_id, limit=100)
#
#     while results:
#         for item in results["items"]:
#             track = item.get("track")
#             if track and track.get("id"):  # Ensure track and track ID exist
#                 tracks.append(track["id"])
#
#         if results["next"]:
#             results = sp.next(results)
#         else:
#             break
#
#     return tracks
#
#
# # Function to split list into chunks of `size`
# def chunkify(lst, size):
#     return [lst[i:i + size] for i in range(0, len(lst), size)]
#
#
# # Function to add tracks in batches of 100
# def add_tracks_in_batches(playlist_id, track_list):
#     track_batches = chunkify(track_list, 100)
#     for batch in track_batches:
#         sp.playlist_add_items(playlist_id=playlist_id, items=batch)
#
#
# # Playlist ID of the source playlist
# source_playlist_id = "0s7WAHI723fLXFZ7fwyj3f"
#
# # Fetch tracks from the playlist (SKIPS None Tracks)
# playlist_songs = get_playlist_tracks(source_playlist_id)
# print(f"✅ Fetched {len(playlist_songs)} valid tracks from playlist {source_playlist_id}.")
#
# # Split into chunks of 300 songs
# track_chunks = chunkify(playlist_songs, 300)
#
# # Create new playlists and add songs
# for i, chunk in enumerate(track_chunks):
#     playlist_name = f"all_songs_i_like_tidal_transfer_playlist_{i + 1}"
#
#     # Create playlist
#     playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
#     playlist_id = playlist["id"]
#
#     # Add tracks in batches of 100
#     add_tracks_in_batches(playlist_id, chunk)
#
#     print(f"✅ Created {playlist_name} with {len(chunk)} tracks.")
#
# print("🎵 All playlists created successfully!")