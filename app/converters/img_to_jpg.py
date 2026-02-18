from io import BytesIO

from PIL import Image


def image_to_jpg(image_bytes: bytes) -> bytes:
    """
    Convert any image (png, webp, bmp, etc.) to JPG bytes
    """

    img = Image.open(BytesIO(image_bytes))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    output = BytesIO()
    img.save(output, format="JPEG", quality=95)

    output.seek(0)
    return output.read()
