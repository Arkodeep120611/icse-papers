import os
import re

SOURCE_FOLDER = "../papers"

def clean_filename(filename):

    name = filename.replace(".pdf", "")

    name = re.sub(r"\s+", " ", name)

    return name.strip()

for year in os.listdir(SOURCE_FOLDER):

    folder = os.path.join(SOURCE_FOLDER, year)

    if not os.path.isdir(folder):
        continue

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            old_path = os.path.join(folder, file)

            cleaned = clean_filename(file)

            new_path = os.path.join(folder, cleaned)

            os.rename(old_path, new_path)

            print(f"Renamed: {file} -> {cleaned}")