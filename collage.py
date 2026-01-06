from PIL import Image
import os

def create_collage(image_paths, output_path):
    images = [Image.open(p).resize((300, 300)) for p in image_paths]

    collage = Image.new("RGB", (600, 600), "#ffd1dc")

    positions = [
        (0, 0),
        (300, 0),
        (0, 300),
        (300, 300)
    ]

    for img, pos in zip(images, positions):
        collage.paste(img, pos)

    collage.save(output_path)
    return output_path
