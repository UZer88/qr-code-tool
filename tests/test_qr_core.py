import pytest
import tempfile
import sys
import os
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qr_core import generate_qr_image, save_qr_image, scan_qr_from_file, scan_qr_from_image


class TestGenerateQR:
    def test_generate_qr_returns_image(self):
        img = generate_qr_image("https://example.com", size=300)
        assert isinstance(img, Image.Image)
        assert img.size[0] == 300
        assert img.size[1] == 300

    def test_generate_qr_with_different_sizes(self):
        for size in [100, 250, 500]:
            img = generate_qr_image("test", size=size)
            assert img.size[0] == size

    def test_generate_qr_empty_text_raises_error(self):
        with pytest.raises(ValueError, match="Text cannot be empty"):
            generate_qr_image("")

    def test_generate_qr_encoding_preserves_data(self):
        original = "Hello, QR World! 123"
        img = generate_qr_image(original)
        decoded = scan_qr_from_image(img)
        assert decoded == original


class TestSaveQR:
    def test_save_qr_to_file(self):
        img = generate_qr_image("test data")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            save_qr_image(img, tmp.name)
            assert os.path.exists(tmp.name)
            assert os.path.getsize(tmp.name) > 0
        os.unlink(tmp.name)


class TestScanQR:
    def test_scan_qr_from_file(self):
        original = "https://github.com/UZer88"
        img = generate_qr_image(original)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp.name)
            decoded = scan_qr_from_file(tmp.name)

        os.unlink(tmp.name)
        assert decoded == original

    def test_scan_qr_from_image_object(self):
        original = "Direct image scan test"
        img = generate_qr_image(original)
        decoded = scan_qr_from_image(img)
        assert decoded == original

    def test_scan_nonexistent_file_raises_error(self):
        with pytest.raises(FileNotFoundError):
            scan_qr_from_file("nonexistent_file.png")

    def test_scan_image_without_qr_raises_error(self):
        # Создаём пустое изображение без QR-кода
        blank_img = Image.new('RGB', (200, 200), color='white')
        with pytest.raises(ValueError, match="No QR code found"):
            scan_qr_from_image(blank_img)