from setuptools import setup, find_packages

setup(
    name="qr-code-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]",
        "pyzbar",
        "pillow",
        "pyperclip",
    ],
    python_requires=">=3.10",
)