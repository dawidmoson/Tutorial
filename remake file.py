import os
import shutil
import re
from setuptools import setup, find_packages

def normalize(filename):
    filename = re.sub(r'[ąęćżźńółęąśżźń]', lambda x: '_' if x.group() in 'ąęćżźńółęąśżźń' else x.group(), filename)
    filename = re.sub(r'[^A-Za-z0-9_.]', '_', filename)
    return filename

def process_folder(folder_path):
    known_extensions = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }
    unknown_extensions = set()
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_extension = os.path.splitext(name)[1][1:].upper()
            if file_extension in known_extensions:
                new_name = normalize(name)
                new_path = os.path.join(root, '..', known_extensions[file_extension][0], new_name)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(file_path, new_path)
            else:
                unknown_extensions.add(file_extension)
        for name in dirs:
            dir_path = os.path.join(root, name)
            if os.path.isdir(dir_path):
                process_folder(dir_path)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

if __name__ == "__main__":
    process_folder('/ścieżka/do/twojego/testowego/folderu')

from setuptools import setup, find_packages

setup(
    name='clean-folder',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.clean:main']
    },
    install_requires=[
        
    ],
)
