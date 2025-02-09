import json

# Sample dictionary
data = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

json_file_path = r"C:\Users\vikaskoppineedi\Desktop\torrents_info.json"
# Define the output file path
file_path = r"C:\Users\vikaskoppineedi\Desktop\ds_torrents_info.json"  # Change as needed


with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

sorted_data = sorted(data, key=lambda x: x["torrentName"])

ds_data = []
for block in sorted_data:
    if "desitorrents" in block["torrentsTags"]:
        ds_data.append(block)
        print(block)

# Write dictionary to JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(ds_data, file, indent=4)  # `indent=4` makes it more readable

print(f"JSON file saved at: {file_path}")