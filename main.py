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

def choose_file(matches):
    print(YELLOW + "\nFound multiple files:")
    for i,path in enumerate(matches,1):
        print(f"{i}. {path}")
        print(RESET)
    while True:
        choice = input("Choose a number (or 'q'):").strip()
        if choice.lower() == 'q':
            return None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                return matches[idx]
        print(RED + "invalid choice" + RESET)


def search_file(filename):
    print(YELLOW + f"[*] Searching {filename}"+ RESET)
    search_paths=[os.path.expanduser("~"),"/madia","/mnt"]
    matches=[]
    for base in search_paths:
        if not os.path.exists(base):
            continue
        for root,_,files in os.walk(base):
            if filename in files:
                matches.append(os.path.join(root,filename))
            if len(matches)>=10:
                return matches
    return matches


def main():
    while True:
        banner()
        raw_input = input("Enter file path or name: ").strip()
           
        if not raw_input:
            continue
        if raw_input.lower() in ["exit", "quit"]:
            break

        if not os.path.isfile(file_path):
            matches = search_file(raw_input)
            if not matches:
                print(RED + "File Not Found" + RESET)
                continue
            elif len(matches) == 1:
                file_path = matches[0]
            else:
                file_path = choose_file(matches)
                if not file_path:
                    continue
             
        file_path = os.path.expanduser(raw_input)
      print(YELLOW + "\n--- METADATA ---")
        for k, v in metadata.items():
            print(f"{k}: {v}")
        print(RESET)




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")