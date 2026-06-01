import os
import shutil
import random
from PIL import Image, ImageOps

# Configuration
SOURCE_DIR = "data/raw"
DEST_DIR = "dataset"
# Split ratios: 70% Train, 15% Val, 15% Test
TRAIN_RATIO, VAL_RATIO = 0.7, 0.15 
IMG_SIZE = (224, 224) 

def prepare_data():
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR) # Clear old dataset

    for split in ["train", "val", "test"]:
        for breed in os.listdir(SOURCE_DIR):
            os.makedirs(os.path.join(DEST_DIR, split, breed), exist_ok=True)

    for breed in os.listdir(SOURCE_DIR):
        breed_path = os.path.join(SOURCE_DIR, breed)
        images = [f for f in os.listdir(breed_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        random.shuffle(images)

        train_split = int(len(images) * TRAIN_RATIO)
        val_split = int(len(images) * (TRAIN_RATIO + VAL_RATIO))

        for i, img_name in enumerate(images):
            if i < train_split: subset = "train"
            elif i < val_split: subset = "val"
            else: subset = "test"
            
            src = os.path.join(breed_path, img_name)
            dst = os.path.join(DEST_DIR, subset, breed, img_name)
            
            try:
                with Image.open(src) as img:
                    # Convert to RGB to handle PNG/Greyscale images
                    img = img.convert("RGB")
                    
                    img_standardized = ImageOps.fit(img, IMG_SIZE, Image.Resampling.LANCZOS)
                    
                    # Save to the destination folder
                    img_standardized.save(dst, "JPEG")
            except Exception as e:
                print(f"Skipping {img_name}: {e}")
        print(f"Processed {breed}: {len(images)} images.")

if __name__ == "__main__":
    prepare_data()