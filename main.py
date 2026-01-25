#!/usr/bin/env python3

import os
import sys

# colors OK 
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(CYAN + "=" * 60)
    print(" " * 18 + "File Metadata Extractor")
    print(" " * 10 + "Extract all Remove only Images")
    print("=" * 60 + RESET)


def is_image(path):
    return path.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp"))


def main():
    while True:
        banner()







if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")