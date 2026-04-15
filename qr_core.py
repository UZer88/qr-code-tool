import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import tempfile
import os


def generate_qr_image(text: str, size: int = 250) -> Image.Image:
    """
    Генерирует QR-код из текста и возвращает объект PIL Image.
    """
    if not text:
        raise ValueError("Text cannot be empty")

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img


def save_qr_image(img: Image.Image, file_path: str) -> None:
    """
    Сохраняет изображение QR-кода в файл.
    """
    img.save(file_path)


def scan_qr_from_file(file_path: str) -> str:
    """
    Сканирует QR-код из файла и возвращает декодированный текст.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    img = Image.open(file_path)
    decoded = decode(img)

    if not decoded:
        raise ValueError("No QR code found in image")

    return decoded[0].data.decode('utf-8')


def scan_qr_from_image(img: Image.Image) -> str:
    """
    Сканирует QR-код из объекта PIL Image.
    """
    decoded = decode(img)
    if not decoded:
        raise ValueError("No QR code found in image")
    return decoded[0].data.decode('utf-8')