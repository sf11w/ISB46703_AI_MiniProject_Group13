import os
import shutil

def reindex_images(base_path):
    for breed in os.listdir(base_path):
        breed_dir = os.path.join(base_path, breed)
        if not os.path.isdir(breed_dir):
            continue

        print(f"Re-indexing {breed}...")
       
        # 1. Create a temporary folder
        temp_dir = os.path.join(breed_dir, "temp_reindex")
        os.makedirs(temp_dir, exist_ok=True)

        # 2. Move all files into the temp folder with new names
        files = sorted([f for f in os.listdir(breed_dir) if f.endswith(".jpg")])

        for index, filename in enumerate(files):
            old_path = os.path.join(breed_dir, filename)
            new_filename = f"{breed}_{index}.jpg"
            new_path = os.path.join(temp_dir, new_filename)
            shutil.move(old_path, new_path)

        # 3. Move files back from temp to the main breed directory
        for filename in os.listdir(temp_dir):
            shutil.move(os.path.join(temp_dir, filename), os.path.join(breed_dir, filename))
       

        # 4. Remove the empty temp folder
        os.rmdir(temp_dir)

if __name__ == "__main__":
    reindex_images(os.path.join("data", "raw"))
    print("All folders have been re-indexed successfully!")