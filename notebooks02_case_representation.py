# notebooks/02_case_representation.py

import os
import re
import pandas as pd
from datetime import datetime


# Path folder teks hasil cleaning dari Tahap 1
TXT_DIR = "data/raw_cleaned"
# Output CSV
OUT_CSV = "data/processed/cases.csv"

# Mapping bulan Indonesia → Inggris untuk strptime
BULAN_MAP = {
    "Januari": "January", "Februari": "February", "Maret": "March",
    "April": "April", "Mei": "May", "Juni": "June",
    "Juli": "July", "Agustus": "August", "September": "September",
    "Oktober": "October", "November": "November", "Desember": "December"
}

def parse_tanggal(tgl_str):
    """
    Ubah bulan Indonesia ke Inggris lalu parse.
    Contoh input: "6 Juni 2017"
    """
    for indo, eng in BULAN_MAP.items():
        if indo in tgl_str:
            tgl_str = tgl_str.replace(indo, eng)
            break
    return datetime.strptime(tgl_str, "%d %B %Y")

def clean_whitespace(s):
    """Helper: trim dan collapse whitespace."""
    return re.sub(r"\s+", " ", s.strip())

records = []

# Loop semua file .txt
for fn in os.listdir(TXT_DIR):
    if not fn.lower().endswith(".txt"):
        continue

    path = os.path.join(TXT_DIR, fn)
    text = open(path, encoding="utf-8").read()

    # --- Ekstraksi Nomor Perkara ---
    m = re.search(r"Nomor\s*[:\-]\s*([^\s,]+)", text)
    no_perkara = m.group(1) if m else None

    # --- Ekstraksi Tanggal Putusan ---
    m = re.search(r"tanggal\s*([0-9]{1,2}\s+\w+\s+[0-9]{4})", text, re.IGNORECASE)
    tanggal = parse_tanggal(clean_whitespace(m.group(1))) if m else None

    # --- Ekstraksi Pasal / Dasar Hukum ---
    pasal_list = re.findall(r"(?:Pasal|UU No\.)\s*[:\-]?\s*([^\n;]+)", text)
    pasal = "; ".join(pasal_list)

    # --- Ekstraksi Nama Pihak / Terdakwa ---
    m = re.search(r"Nama\s+lengkap\s*[:\-]\s*(.+)", text)
    if not m:
        m = re.search(r"Nama\s*[:\-]\s*(.+)", text)
    pihak = clean_whitespace(m.group(1)) if m else ""

    # --- Ringkasan Fakta: semua sebelum "Menimbang" ---
    ringkasan = text.split("Menimbang", 1)[0]
    ringkasan = clean_whitespace(ringkasan)[:800]  # potong 800 char untuk ringkas

    # --- Ekstraksi Amar Putusan ---
    sol = ""
    # Cari hukuman penjara
    m2 = re.search(r"Menjatuhkan\s+pidana\s+penjara\s+selama\s+([^\n]+)", text)
    if m2:
        sol = "penjara " + clean_whitespace(m2.group(1))
    else:
        # fallback: cari kata "Menetapkan"
        m3 = re.search(r"Menetapkan\s*[:\-]\s*([^\n]+)", text)
        if m3:
            sol = clean_whitespace(m3.group(1))

    # Simpan record
    records.append({
        "case_id": fn[:-4],
        "no_perkara": no_perkara,
        "tanggal": tanggal,
        "pasal": pasal,
        "pihak": pihak,
        "ringkasan": ringkasan,
        "text_full": text,
        "amar_putusan": sol
    })

# Buat DataFrame dan ekspor ke CSV
df = pd.DataFrame(records)
output_dir = os.path.dirname(OUT_CSV)
os.makedirs(output_dir, exist_ok=True)
df = pd.DataFrame(records)
df.to_csv(OUT_CSV, index=False)
print(f"[Saved] {OUT_CSV}")
