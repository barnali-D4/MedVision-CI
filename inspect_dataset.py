
from pathlib import Path

DATASET_ROOT = Path(
    r"C:\Users\barna\.cache\kagglehub\datasets"
    r"\paultimothymooney\chest-xray-pneumonia\versions\2"
)

if not DATASET_ROOT.exists():
    raise FileNotFoundError(f"Dataset folder not found: {DATASET_ROOT}")

print(f"Dataset location: {DATASET_ROOT}")
print("\nTop-level contents:")

for item in DATASET_ROOT.iterdir():
    print(" -", item.name)

print("\nImage counts by split and class:")

image_extensions = {".jpg", ".jpeg", ".png"}

for split in ("train", "val", "test"):
    split_path = DATASET_ROOT / "chest_xray" / split

    if not split_path.exists():
        split_path = DATASET_ROOT / split

    if not split_path.exists():
        print(f"\n{split}: folder not found")
        continue

    print(f"\n{split.upper()}")

    for class_name in ("NORMAL", "PNEUMONIA"):
        class_path = split_path / class_name

        if class_path.exists():
            count = sum(
                1 for file in class_path.iterdir()
                if file.is_file()
                and file.suffix.lower() in image_extensions
            )
            print(f"  {class_name}: {count} images")
        else:
            print(f"  {class_name}: folder not found")
