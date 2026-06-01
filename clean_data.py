import os
from PIL import Image

base_path = "data/raw"
MIN_SIZE_BYTES = 5000  # Delete files smaller than 5KB (usually junk)

def clean_images():
    for breed in os.listdir(base_path):
        breed_dir = os.path.join(base_path, breed)
        if not os.path.isdir(breed_dir):
            continue
            
        print(f"Cleaning {breed}...")
        for filename in os.listdir(breed_dir):
            filepath = os.path.join(breed_dir, filename)
            
            # 1. Delete tiny/junk files
            if os.path.getsize(filepath) < MIN_SIZE_BYTES:
                os.remove(filepath)
                continue
                
            # 2. Check for corrupted images
            try:
                with Image.open(filepath) as img:
                    img.verify() # Verify it's a real image
            except (IOError, SyntaxError):
                print(f"Deleting corrupted file: {filename}")
                os.remove(filepath)

if __name__ == "__main__":
    clean_images()
    print("Cleanup complete!")