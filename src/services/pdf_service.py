from PIL import Image
import os


def convert_image_to_pdf(input_path: str, output_path: str) -> str | None:
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        img = Image.open(input_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path)
        return output_path
