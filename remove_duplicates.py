import os
import hashlib

def get_file_hash(filepath):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def remove_duplicates(base_path):
    seen_hashes = set()
    for breed in os.listdir(base_path):
        breed_dir = os.path.join(base_path, breed)
        if not os.path.isdir(breed_dir):
            continue
            
        print(f"Removing duplicates in {breed}...")
        for filename in os.listdir(breed_dir):
            filepath = os.path.join(breed_dir, filename)
            file_hash = get_file_hash(filepath)
            
            if file_hash in seen_hashes:
                os.remove(filepath)
            else:
                seen_hashes.add(file_hash)

if __name__ == "__main__":
    remove_duplicates("data/raw")
    print("Deduplication complete!")