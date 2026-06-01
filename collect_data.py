import asyncio
import os
import requests
from ddgs import DDGS
from crawl4ai import AsyncWebCrawler

# Configuration
base_path = "data/raw"
breeds_queries = {
    "bengal": ["bengal cat", "bengal cat kitten", "bengal cat face", "bengal cat walking", "bengal cat marble pattern", "bengal cat spotted", "bengal cat high resolution", "bengal cat jumping", "bengal cat climbing", "bengal cat resting", "bengal cat close up"],
    "british_shorthair": ["british shorthair cat", "british shorthair kitten", "british shorthair blue", "british shorthair face", "british shorthair chunky", "british shorthair grey cat", "british shorthair sitting", "british shorthair playing", "british shorthair indoor", "british shorthair adult"],
    "maine_coon": ["maine coon cat", "maine coon kitten", "large maine coon cat", "maine coon cat face", "maine coon ear tufts", "maine coon fluffy", "maine coon jumping", "maine coon climbing", "maine coon outdoor", "maine coon tail"],
    "persian": ["persian cat", "persian cat kitten", "white persian cat", "persian cat face", "persian cat long hair", "flat face persian cat", "persian cat sleeping", "persian cat playing", "persian cat show", "persian cat fluffy"],
    "ragdoll": ["ragdoll cat", "ragdoll kitten", "ragdoll cat eyes", "ragdoll cat face", "ragdoll cat blue eyes", "ragdoll cat bicolor", "ragdoll cat carrying", "ragdoll cat lounging", "ragdoll cat lying down", "ragdoll cat sweet"],
    "siamese": ["siamese cat", "siamese kitten", "siamese cat pointed", "siamese cat face", "siamese cat seal point", "siamese cat elegant", "siamese cat active", "siamese cat talking", "siamese cat Siamese blue eyes", "siamese cat profile"],
    "sphynx": ["sphynx cat", "sphynx kitten", "sphynx cat face", "sphynx cat sitting", "sphynx cat skin", "hairless cat portrait", "sphynx cat sweater", "sphynx cat playing", "sphynx cat warm", "sphynx cat close up"]
}

def download_with_requests(img_url, file_path):
    """Tier 1: Fast download using requests."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(img_url, headers=headers, timeout=5)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            return True
    except:
        return False
    return False

async def download_with_crawl4ai(crawler, img_url, file_path):
    """Tier 2: Browser-based fallback using Crawl4AI."""
    try:
        result = await crawler.arun(url=img_url)
        if result.binary_data:
            with open(file_path, "wb") as f:
                f.write(result.binary_data)
            return True
    except:
        return False
    return False

async def main():
    async with AsyncWebCrawler() as crawler:
        with DDGS() as ddgs:
            for breed, queries in breeds_queries.items():
                print(f"\n--- Starting {breed} ---")
                breed_dir = os.path.join(base_path, breed)
                os.makedirs(breed_dir, exist_ok=True)
                
                # Smart Counting
                existing_files = [f for f in os.listdir(breed_dir) if f.endswith(".jpg")]
                count = len(existing_files)
                
                for query in queries:
                    print(f"Searching: {query}...")
                    results = ddgs.images(query, max_results=50)
                    
                    for result in results:
                        img_url = result["image"]
                        file_name = os.path.join(breed_dir, f"{breed}_{count}.jpg")
                        
                        if os.path.exists(file_name):
                            continue
                        
                        # Execute Two-Tier Download Logic
                        if download_with_requests(img_url, file_name):
                            count += 1
                        elif await download_with_crawl4ai(crawler, img_url, file_name):
                            count += 1
                        
                        await asyncio.sleep(2) # Politeness delay
                
                print(f"Finished {breed}. Total images for this breed: {count}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())