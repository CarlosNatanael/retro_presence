from PIL import Image
import os

def resize_image(input_path, output_path, width=1024, height=576, format="PNG"):
    img = Image.open(input_path)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    valid_formats = ["PNG", "JPG", "WEBP"]
    if format.upper() not in valid_formats:
        raise ValueError(f"Formato inválido. Use um destes: {valid_formats}")
    img.save(output_path, format=format.upper(), optimize=True)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    if size_mb > 10:
        raise ValueError("A imagem ultrapassa o tamanho máximo de 10MB.")
resize_image("ralibretro_logo.png", "saida.png", format="PNG")