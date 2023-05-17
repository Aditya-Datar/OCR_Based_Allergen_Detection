from PIL import Image

def get_image_orientation(image_path):
    image = Image.open(image_path)

    # Check if the image has an Exif tag for orientation
    if hasattr(image, '_getexif') and image._getexif() is not None:
        exif_data = image._getexif()
        orientation_tag = 274  # Exif tag for orientation

        # If the orientation tag exists in the Exif data
        if orientation_tag in exif_data:
            orientation = exif_data[orientation_tag]

            # Determine the orientation value and return a description
            if orientation == 1:
                return "Normal"
            elif orientation == 2:
                return "Flipped horizontally"
            elif orientation == 3:
                return "Rotated 180 degrees"
            elif orientation == 4:
                return "Flipped vertically"
            elif orientation == 5:
                return "Rotated 90 degrees counterclockwise and flipped horizontally"
            elif orientation == 6:
                return "Rotated 270 degrees"
            elif orientation == 7:
                return "Rotated 90 degrees clockwise and flipped horizontally"
            elif orientation == 8:
                return "Rotated 90 degrees clockwise"
    
    # Default case if the orientation cannot be determined
    return "Unknown"

# Example usage
image_path = r"C:\Users\Aditya Datar\Desktop\Semester 8\Final Year Project\Codes\uploads\img_optimized.jpg"
orientation = get_image_orientation(image_path)
print("Image orientation:", orientation)
