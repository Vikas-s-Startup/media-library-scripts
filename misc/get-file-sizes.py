import os


def get_size_in_human_readable_format(size_in_bytes):
    """Convert size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def calculate_folder_size(folder_path):
    """Calculate the total size of a folder."""
    total_size = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def convert_to_bytes(size, unit):
    """Convert size with a unit to bytes."""
    units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
    return size * units[unit.upper()]


def list_folders_below_size(directory_path, max_size_in_bytes):
    """List all folders in the given directory with sizes below the threshold."""
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    print(f"Listing folders below {get_size_in_human_readable_format(max_size_in_bytes)} in '{directory_path}':\n")
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path):
            folder_size = calculate_folder_size(folder_path)
            if folder_size < max_size_in_bytes:
                human_readable_size = get_size_in_human_readable_format(folder_size)
                print(f"{folder_name} - {human_readable_size}")


# Configurable Parameters
target_directory = r"E:\Movies\IMDB-TOP-250/"
size_limit = 10  # Specify the size limit
size_unit = "GB"  # Units can be "B", "KB", "MB", "GB", "TB"

# Convert the size limit to bytes
max_size_in_bytes = convert_to_bytes(size_limit, size_unit)

# Run the folder size filter
list_folders_below_size(target_directory, max_size_in_bytes)
