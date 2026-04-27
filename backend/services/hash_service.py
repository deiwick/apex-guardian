import os
import io
import imagehash
from PIL import Image

def generate_phash_from_image(file_bytes: bytes) -> str:
    """
    Generate a perceptual hash limit for an image.
    Currently applies purely to images for proof of concept.
    For video processing, one would sample frames and aggregate hashes.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        phash = imagehash.phash(image)
        return str(phash)
    except Exception as e:
        print(f"Error generating pHash: {e}")
        return None
