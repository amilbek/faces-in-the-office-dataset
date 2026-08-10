import os
import shutil
import random
import csv
from pathlib import Path

# --- CONFIG ---
SRC_DIR = Path("face_crops_persons") 
GALLERY_DIR = Path("database")
QUERY_DIR = Path("test")
SPLIT_CSV = Path("gallery_query_split.csv")
GALLERY_RATIO = 0.55
SEED = 42
# --------------

random.seed(SEED)

GALLERY_DIR.mkdir(exist_ok=True)
QUERY_DIR.mkdir(exist_ok=True)

rows = []

for person_dir in sorted(SRC_DIR.iterdir()):
    if not person_dir.is_dir():
        continue

    identity = person_dir.name
    images = sorted([f for f in person_dir.iterdir() if f.suffix.lower() == ".jpg"])
    random.shuffle(images)

    n_gallery = round(len(images) * GALLERY_RATIO)
    gallery_files = images[:n_gallery]
    query_files = images[n_gallery:]

    (GALLERY_DIR / identity).mkdir(exist_ok=True)
    (QUERY_DIR / identity).mkdir(exist_ok=True)

    for f in gallery_files:
        shutil.copy2(f, GALLERY_DIR / identity / f.name)
        rows.append({"identity_id": identity, "filename": f.name, "split": "gallery"})

    for f in query_files:
        shutil.copy2(f, QUERY_DIR / identity / f.name)
        rows.append({"identity_id": identity, "filename": f.name, "split": "query"})

    print(f"{identity}: {len(gallery_files)} gallery, {len(query_files)} query "
          f"({len(gallery_files)/len(images)*100:.1f}% / {len(query_files)/len(images)*100:.1f}%)")

with open(SPLIT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["identity_id", "filename", "split"])
    writer.writeheader()
    writer.writerows(rows)

total = len(rows)
n_gallery_total = sum(1 for r in rows if r["split"] == "gallery")
n_query_total = total - n_gallery_total
print()
print(f"TOTAL: {total} images")
print(f"Gallery: {n_gallery_total} ({n_gallery_total/total*100:.1f}%)")
print(f"Query: {n_query_total} ({n_query_total/total*100:.1f}%)")
print(f"Saved split index to {SPLIT_CSV}")
