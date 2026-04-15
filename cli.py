#!/usr/bin/env python3
# cli.py
import argparse
import sys
from qr_core import generate_qr_image, save_qr_image, scan_qr_from_file


def main():
    parser = argparse.ArgumentParser(description="QR Code Tool - CLI version")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Генерация QR
    gen_parser = subparsers.add_parser("generate", help="Generate QR code")
    gen_parser.add_argument("text", help="Text or URL to encode")
    gen_parser.add_argument("-s", "--size", type=int, default=250, help="QR code size (default: 250)")
    gen_parser.add_argument("-o", "--output", default="qr_code.png", help="Output file name")

    # Сканирование QR
    scan_parser = subparsers.add_parser("scan", help="Scan QR code from image")
    scan_parser.add_argument("image", help="Path to image file")

    args = parser.parse_args()

    if args.command == "generate":
        img = generate_qr_image(args.text, args.size)
        save_qr_image(img, args.output)
        print(f"✅ QR code saved to {args.output}")

    elif args.command == "scan":
        try:
            result = scan_qr_from_file(args.image)
            print(f"📄 Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()