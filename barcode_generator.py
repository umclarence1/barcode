import os
import uuid
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

# === Configuration ===
PHOTO_DIR = "tray_photos"
BARCODE_DIR = "barcodes"
TSC_FILE = "barcode_output.tsc"
os.makedirs(BARCODE_DIR, exist_ok=True)

def generate_unique_id():
    return str(uuid.uuid4())[:8]  # Shortened UUID

def generate_barcode_image(code: str, output_path: str):
    barcode = Code128(code, writer=ImageWriter())
    barcode.save(output_path)

def process_tray_photos():
    print("🔍 Scanning tray_photos/")
    if not os.path.exists(PHOTO_DIR):
        print("❌ 'tray_photos/' folder not found.")
        return

    files = os.listdir(PHOTO_DIR)
    print(f"📂 Found {len(files)} files")

    with open(TSC_FILE, "w") as tsc:
        tsc.write("IMAGE_NAME,BARCODE_ID\n")

        for filename in files:
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            unique_id = generate_unique_id()
            barcode_path = os.path.join(BARCODE_DIR, f"{unique_id}")

            generate_barcode_image(unique_id, barcode_path)
            tsc.write(f"{filename},{unique_id}\n")

            print(f"✅ Processed {filename} -> Barcode ID: {unique_id}")

if __name__ == "__main__":
    process_tray_photos()
