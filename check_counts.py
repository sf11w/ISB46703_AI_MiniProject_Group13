import os
base_path = os.path.join("data", "raw")

for breed in os.listdir(base_path):
    breed_dir = os.path.join(base_path, breed)
    if os.path.isdir(breed_dir):
        count = len([f for f in os.listdir(breed_dir) if f.endswith(".jpg")])
        print(f"{breed}: {count} images")