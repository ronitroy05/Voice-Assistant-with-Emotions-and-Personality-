import asyncio
import os
from random import randint
from PIL import Image
import requests
from dotenv import get_key
from time import sleep

# Ensure required folders exist
os.makedirs("Data", exist_ok=True)
os.makedirs("Frontend/Files", exist_ok=True)

# Ensure ImageGeneration.data file exists
file_path = "Frontend/Files/ImageGeneration.data"
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("TestPrompt,False")  # Default content

# API Config
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_KEY = get_key('.env', 'HuggingFaceAPIKey')
headers = {"Authorization": f"Bearer {API_KEY}"}

async def query(payload):
    """ Send request to API and return image bytes """
    await asyncio.sleep(2)  # ⏳ Wait 2 seconds between requests (Fix rate limit issue)
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)

    if response.status_code == 429:
        print("⚠️ Too Many Requests! Waiting 60 seconds...")
        await asyncio.sleep(60)  # 🕒 Wait for 60 seconds if rate limited
        return await query(payload)  # 🔄 Retry after cooldown

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None  # Return None if API fails

    return response.content

async def generate_images(prompt: str):
    """ Generate 4 images from the given prompt """
    tasks = []
    prompt = prompt.replace(" ", "_")

    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes is None:
            print(f"Image {i+1} generation failed.")
            continue

        file_path = f"Data/{prompt}{i + 1}.jpg"
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print(f"✅ Image saved: {file_path}")

    open_images(prompt)

def open_images(prompt):
    """ Open generated images one by one """
    prompt = prompt.replace(" ", "_")
    for i in range(1, 5):
        image_path = f"Data/{prompt}{i}.jpg"
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                print(f"📷 Opening: {image_path}")
                img.show()
                sleep(1)
            except IOError:
                print(f"❌ Unable to open {image_path}")
        else:
            print(f"❌ File not found: {image_path}")

def main():
    """ Main function to read prompt from file and generate images """
    while True:
        try:
            with open("Frontend/Files/ImageGeneration.data", "r") as f:
                data = f.read().strip()

            if not data:
                sleep(1)
                continue

            prompt, status = data.split(",")
            
            if status.strip().lower() == "true":
                print("🔄 Generating Images... ")
                asyncio.run(generate_images(prompt))

                with open("Frontend/Files/ImageGeneration.data", "w") as f:
                    f.write("False,False")
                
                break  # Exit loop after generation

            else:
                sleep(1)

        except Exception as e:
            print(f"❌ Error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()
