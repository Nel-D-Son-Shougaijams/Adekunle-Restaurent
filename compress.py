from PIL import Image
import os

def compress_images(input_folder, output_folder, quality=60):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filepath = os.path.join(root, file)
                print(f"Compressing: {filepath}")
                try:
                    img = Image.open(filepath)
                    img = img.convert("RGB")  # Ensure compatibility
                    output_path = os.path.join(output_folder, file)
                    img.save(output_path, optimize=True, quality=quality)
                except Exception as e:
                    print(f"Error compressing {filepath}: {e}")

# Input and output folder paths
input_folder = "media"
output_folder = "media"

# Compress images
compress_images(input_folder, output_folder)