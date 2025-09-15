import os
import shutil

# Define folders by file type
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".csv"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Others": []
}

def sort_files(folder_path):
    sorted_files = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            moved = False
            for folder, extensions in FILE_TYPES.items():
                if any(filename.lower().endswith(ext) for ext in extensions):
                    dest_folder = os.path.join(folder_path, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(filepath, os.path.join(dest_folder, filename))
                    sorted_files.append((filename, folder))
                    moved = True
                    break
            if not moved:
                dest_folder = os.path.join(folder_path, "Others")
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(filepath, os.path.join(dest_folder, filename))
                sorted_files.append((filename, "Others"))
    return sorted_files

