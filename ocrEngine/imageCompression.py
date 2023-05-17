from PIL import Image
import os

def compress_image(input_path, target_size):
    image = Image.open(input_path)
    output_path = input_path
    # Set an initial quality level
    quality = 80
    if not os.path.exists(output_path):
        # Save the image with the current quality level
        image.save(output_path, optimize=True, quality=quality)
    
    while os.path.exists(output_path) and os.path.getsize(output_path) > target_size:
        print("IN WHILE")
        # Save the image with the current quality level
        image.save(output_path, optimize=True, quality=quality)

        # Reduce the quality level by 10 units
        quality -= 10

        # Break the loop if the quality level reaches 0
        if quality <= 0:
            break

