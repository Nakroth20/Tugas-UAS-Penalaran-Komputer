import os
from pdfminer.high_level import extract_text

RAW_DIR   = r"D:\Project Penalaran Komputer\Data\raw"
CLEAN_DIR = r"D:\Project Penalaran Komputer\Data\raw_cleaned"

CLEAN_DIR   = "data/raw_cleaned"
os.makedirs(CLEAN_DIR, exist_ok=True)

def pdf_to_txt(pdf_path, txt_path):
    text = extract_text(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

def clean_text(text):
    # Contoh cleaning sederhana: hapus header/footer & watermark
    import re
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line: 
            continue
        # hapus watermark MA RI
        if line.startswith("Mah") or line.startswith("Direktori"):
            continue
        # hapus nomor halaman
        if re.match(r"^Hal\s*\d+\s+dari", line):
            continue
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    # 1) PDF → TXT
    for fn in os.listdir(RAW_DIR):
        if fn.lower().endswith(".pdf"):
            pdf_path = os.path.join(RAW_DIR, fn)
            txt_path = os.path.join(RAW_DIR, fn[:-4] + ".txt")
            pdf_to_txt(pdf_path, txt_path)
            print(f"[PDF→TXT] {pdf_path}")

    # 2) Cleaning
    for fn in os.listdir(RAW_DIR):
        if fn.lower().endswith(".txt"):
            raw_txt = open(os.path.join(RAW_DIR, fn), encoding="utf-8").read()
            cleaned = clean_text(raw_txt)
            with open(os.path.join(CLEAN_DIR, fn), "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"[Clean] {fn}")
