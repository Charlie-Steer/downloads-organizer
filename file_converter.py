from PIL import Image
import os, sys

# Convert image file to png
def convert_to_png(file_path):
    image = Image.open(file_path)
    output_path = os.path.splitext(file_path)[0] + '.png'
    print("output filepath: "+output_path)
    return image, output_path

def save_image(image, output_path, original_file=None, delete_original=False):
    # Save the image
    image.save(output_path)
    if delete_original:
        os.remove(original_file)



if __name__ == "__main__":
    newImage, path = convert_to_png(sys.argv[1]) # BUG: index out of range
    save_image(newImage, path)
