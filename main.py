import os
import shutil
from collections import defaultdict

def process_files(input_folder, output_base):
    # Define output folders
    folders = [
        "Manual",
        "Mot 2nd",
        "Mot Alt",
        "Full Set",
        "Review",
        "DJ",        # <-- New DJ-related folder
        "Issue"
    ]

    # Create folders
    for folder in folders:
        os.makedirs(os.path.join(output_base, folder), exist_ok=True)

    # Group files by file number
    file_map = defaultdict(list)

    for filename in os.listdir(input_folder):
        if not os.path.isfile(os.path.join(input_folder, filename)):
            continue
        if '-' not in filename:
            continue

        file_number = filename.split('-')[0].strip()
        file_map[file_number].append(filename)

    # Sort each group
    for file_number, files in file_map.items():
        filenames_lower = [f.lower() for f in files]

        # === Rule 1: Any file is 'fileNumber-att'
        if any(f.lower().startswith(f"{file_number.lower()}-att") for f in files):
            destination = "Manual"

        # === Rule 6 (new): Any file ends with -dj, -jmt, or -cj
        elif any(f.lower().startswith(f"{file_number.lower()}-{suffix}") for f in files for suffix in ["dj", "jmt", "cj", "renewal"]):
            destination = "DJ"

        # === Rule 2: Full Set
        elif all(any(key in f for f in filenames_lower)
                 for key in ["mot 2nd", "other2nd", "mot alt", "ord alt"]):
            destination = "Full Set"

        # === Rule 3: mot 2nd + other2nd (2 files only)
        elif "mot 2nd" in " ".join(filenames_lower) and "other2nd" in " ".join(filenames_lower) and len(files) == 2:
            destination = "Mot 2nd"

        # === Rule 4: mot alt + ord alt (2 files only)
        elif "mot alt" in " ".join(filenames_lower) and "ord alt" in " ".join(filenames_lower) and len(files) == 2:
            destination = "Mot Alt"

        # === Rule 5: Single file
        elif len(files) == 1:
            destination = "Review"

        # === Fallback
        else:
            destination = "Issue"

        # Move all files for this group
        for file in files:
            src = os.path.join(input_folder, file)
            dest = os.path.join(output_base, destination, file)
            shutil.move(src, dest)
