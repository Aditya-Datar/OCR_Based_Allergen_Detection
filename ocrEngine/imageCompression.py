from PIL import Image,ImageOps
import os

def compress_image(input_path, target_size):
    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)
    # Set an initial quality level
    quality = 100
    while os.path.exists(input_path) and os.path.getsize(input_path) > target_size:
        print("Compressing Image")
        print(os.path.getsize(input_path))
        # Save the image with the current quality level
        image.save(input_path, optimize=True, quality=quality)

        # Reduce the quality level by 10 units
        quality -= 10

        # Break the loop if the quality level reaches 0
        if quality <= 0:
            break
    image = ImageOps.exif_transpose(image)