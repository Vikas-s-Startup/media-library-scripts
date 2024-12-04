import qbittorrentapi
import json
import os

# instantiate a Client using the appropriate WebUI configuration
conn_info = dict(
	host="192.168.50.121",
	port=9999,
	username="admin",
	password="123456",
)
qbt_client = qbittorrentapi.Client(**conn_info)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
	qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
	print(e)

torrent_files_dir = os.path.join(os.getcwd(), "Torrent-files")
os.makedirs(torrent_files_dir, exist_ok=True)
# Prepare data for JSON file
torrents_data = []

for torrent in qbt_client.torrents_info():
	torrent_file_path = os.path.join(torrent_files_dir, f"{torrent.name}.torrent")

	# Export the torrent file to the specified folder
	try:
		with open(torrent_file_path, "wb") as torrent_file:
			torrent_file.write(qbt_client.torrents_export(torrent_hash=torrent.hash))
		print(f"Exported {torrent.name}.torrent to {torrent_file_path}")
	except Exception as e:
		print(f"Failed to export {torrent.name}: {e}")

	# Add torrent information to JSON structure
	torrent_info = {
		"torrentName": torrent.name,
		"torrentFileName": f"{torrent.name}.torrent",
		"torrentSaveLocation": torrent.save_path,
		"torrentsTags": torrent.tags.split(",") if torrent.tags else []
	}
	torrents_data.append(torrent_info)

# Define the path to save the JSON file in the current directory
json_file_path = os.path.join(os.getcwd(), "torrents_info.json")

# Write data to JSON file
with open(json_file_path, "w") as json_file:
	json.dump(torrents_data, json_file, indent=4)

print(f"Data has been written to {json_file_path}")

# Write data to JSON file
with open(json_file_path, "w") as json_file:
	json.dump(torrents_data, json_file, indent=4)

print(f"Data has been written to {json_file_path}")
