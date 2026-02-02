#!/usr/bin/env python3

import os
import sys
import subprocess
import exifread
from PIL import Image
try:
    import readline
except ImportError:
    pass
# هذا الوان
# colors OK 
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
# هذاالداله يعمل يمسح الذي في الشاشه السودا ويعمل شكل واجهه
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(CYAN + "=" * 60)
    print(" " * 18 + "File Metadata Extractor")
    print(" " * 10 + "Extract all Remove only Images")
    print("=" * 60 + RESET)
    # استخراج البيانات
def extract_metadata(path):
    metadata = {}

    stat = os.stat(path)
    metadata["File Size"] = f"{stat.st_size} bytes"
    metadata["Created"] = str(stat.st_ctime)
    metadata["Modified"] = str(stat.st_mtime)
    metadata["Permissions"] = oct(stat.st_mode)

    if is_image(path):
        try:
            with open(path, "rb") as f:
                tags = exifread.process_file(f, details=False)
                for tag in tags:
                    metadata[f"EXIF:{tag}"] = str(tags[tag])
        except Exception as e:
            metadata["EXIF Error"] = str(e)

    try:
        result = subprocess.run(
            ["exiftool", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in result.stdout.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                metadata[f"Tool:{k.strip()}"] = v.strip()
    except FileNotFoundError:
        metadata["Info"] = "exiftool not installed (system metadata only)"

    return metadata
# داله تحقق انها صوره
def is_image(path):
    return path.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp"))
# داله في حاله وجود اكثر من ملف بنفس الاسم ومختلف المواقع
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

#داله تبحث عن الملف
def search_file(filename):
    print(YELLOW + f"[*] Searching {filename}"+ RESET)
    search_paths=[os.path.expanduser("~"),"/media","/mnt"]
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
# داله حذف بيانات الصور
def remove_image_metadata(path):
    try:
        img = Image.open(path)
        base, ext = os.path.splitext(path)
        new_file = base + "_cleaned" + ext
        img.save(new_file, exif=b"")
        print(GREEN + f"[+] Clean image saved: {new_file}" + RESET)
    except Exception as e:
        print(RED + f"[-] Error: {e}" + RESET)
    input("Press ENTER to continue...")

# لاخذ عمل مجلد
def get_information_dir():
    info_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Information")
    os.makedirs(info_dir, exist_ok=True)
    return info_dir
# داله تاكد من الحفظ ملف وعدم التكرار
def unique_txt_name(base, directory):
    name = base
    counter = 1
    while os.path.exists(os.path.join(directory, f"{name}.txt")):
        name = f"{base}_{counter}"
        counter += 1
    return os.path.join(directory, f"{name}.txt")
# داله حفظ معلومات في سطح المكتب
def save_metadata(path, metadata):
    info_dir = get_information_dir()
    base = os.path.splitext(os.path.basename(path))[0]
    txt_file = unique_txt_name(base, info_dir)

    with open(txt_file, "w", encoding="utf-8") as f:
        for k, v in metadata.items():
            f.write(f"{k}: {v}\n")

    print(GREEN + f"[+] Saved to: {txt_file}" + RESET)
    input("Press ENTER to continue...")

#داله الرئيسيه
def main():
    while True:
        banner()
        raw_input = input("Enter file path or name: ").strip().strip("'\"")
           
        if not raw_input:
            continue
        if raw_input.lower() in ["exit", "quit"]:
            break
        file_path = os.path.expanduser(raw_input)

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
        metadata = extract_metadata(file_path)
        
        print(YELLOW + "\n--- METADATA ---")
        for k, v in metadata.items():
            print(f"{k}: {v}")
        print(RESET)



# ال main من هنا يشتغل البرنامج
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")