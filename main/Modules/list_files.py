import os

def list_files_and_folders(start_path, indent=0):
    try:
        for item in os.listdir(start_path):
            item_path = os.path.join(start_path, item)
            print("  " * indent + f"- {item}")
            if os.path.isdir(item_path):
                list_files_and_folders(item_path, indent + 1)
    except PermissionError:
        print("  " * indent + f"- [Permission Denied]")

# Specify the directory to start
start_directory = input("Enter the directory path to list: ").strip()

if os.path.isdir(start_directory):
    print(f"Listing all files and folders under: {start_directory}")
    list_files_and_folders(start_directory)
else:
    print(f"The path '{start_directory}' is not a valid directory.")
