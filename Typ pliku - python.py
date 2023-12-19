import os
import shutil
import re

import sys
if len(sys.argv) > 1:
    path = sys.argv[1]
    if os.path.isdir(path):
        print(f"Posortuję folder {path}")
    else:
        print("Podana ścieżka nie jest folderem")
        sys.exit()
else:
    path = "C:/Users/Dawid/Do przejrzenia"
    print(f"Nie podałeś ścieżki do folderu, więc użyję domyślnej: {path}")

extensions = {
    "jpg": "images",
    "png": "images",
    "gif": "images",
    "svg": "images",
    "avi": "video",
    "mp4": "video",
    "mov": "video",
    "mkv": "video",
    "doc": "documents",
    "docx": "documents",
    "txt": "documents",
    "pdf": "documents",
    "xlsx": "documents",
    "pptx": "documents",
    "mp3": "music",
    "ogg": "music",
    "wav": "music",
    "amr": "music",
    "zip": "archives",
    "gz": "archives",
    "tar": "archives",
}

def process_folder(folder):
    files_by_category = {}
    known_extensions = set()
    unknown_extensions = set()
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isdir(file_path):
            process_folder(file_path)
        else:
            file_extension = os.path.splitext(file)[1].lower().strip(".")
            if file_extension in extensions:
                known_extensions.add(file_extension)
                file_category = extensions[file_extension]
                if file_category not in files_by_category:
                    files_by_category[file_category] = []
                files_by_category[file_category].append(file)
                category_folder = os.path.join(folder, file_category)
                if not os.path.isdir(category_folder):
                    os.mkdir(category_folder)
                shutil.move(file_path, category_folder)
            else:
                unknown_extensions.add(file_extension)
                unknown_folder = os.path.join(folder, "unknown")
                if not os.path.isdir(unknown_folder):
                    os.mkdir(unknown_folder)
                shutil.move(file_path, unknown_folder)
    pattern = re.compile(r"[^\w\s\-\.]")
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        new_item = pattern.sub("", item)
        new_item_path = os.path.join(folder, new_item)
        os.rename(item_path, new_item_path)
    print(f"Posortowałem folder {folder}")
    print(f"Lista plików w każdej kategorii:")
    for category, files in files_by_category.items():
        print(f"- {category}: {len(files)} plików")
        for file in files:
            print(f"  - {file}")
    print(f"Wykaz wszystkich znanych rozszerzeń plików: {', '.join(known_extensions)}")
    print(f"Wykaz wszystkich nieznanych rozszerzeń plików: {', '.join(unknown_extensions)}")

process_folder(path)
