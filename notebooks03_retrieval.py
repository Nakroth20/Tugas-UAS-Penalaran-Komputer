# notebooks03_retrieval.py

import os
import re
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── 1) Load dan persiapan case base ────────────────────────────────
CSV_PATH = "data/processed/cases.csv"
df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} cases from {CSV_PATH}")

# Jika kolom amar_putusan kosong, ekstrak dari text_full
def extract_amar(text: str) -> str:
    for pat in [r"(Menjatuhkan.*)",
                r"(Mengabulkan.*)",
                r"(Menolak.*)",
                r"(Menyatakan.*)",
                r"(Menerima permohonan.*)"]:
        m = re.search(pat, text or "")
        if m:
            return m.group(1).strip()
    return ""

if "amar_putusan" not in df.columns:
    df["amar_putusan"] = ""

df["amar_putusan"] = df.apply(
    lambda r: r["amar_putusan"] 
              if pd.notna(r["amar_putusan"]) and r["amar_putusan"]!="" 
              else extract_amar(r.get("text_full","")),
    axis=1
)

# ─── 2) Preprocessing & TF-IDF ─────────────────────────────────────
def preproc(s: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())

df["proc_text"] = df["text_full"].fillna("").apply(preproc)

tfidf = TfidfVectorizer(ngram_range=(1,2))
X_tfidf = tfidf.fit_transform(df["proc_text"])

# ─── 3) Retrieval function w/ fallback substring ─────────────────
def retrieve(query: str, k: int = 1):
    q = preproc(query)
    qv = tfidf.transform([q])
    sims = cosine_similarity(qv, X_tfidf).flatten()
    if sims.max() > 0:
        idx = sims.argsort()[-k:][::-1]
    else:
        counts = df["proc_text"].apply(lambda d: d.count(q))
        idx = counts.sort_values(ascending=False).index[:k]
    return [
        {
            "case_id":      df.at[i, "case_id"],
            "amar_putusan": df.at[i, "amar_putusan"]
        }
        for i in idx
    ]

# ─── 4) Load queries & run retrieval ───────────────────────────────
with open("data/eval/queries.json", encoding="utf-8") as f:
    queries = json.load(f)

rows = []
for q in queries:
    # ambil id, fallback ke query_id jika id tak ada
    qid = q.get("id") or q.get("query_id")
    top = retrieve(q["query"], k=1)[0]
    rows.append({
        "query_id":       qid,
        "query_text":     q["query"],
        "retrieved_case": top["case_id"],
        "pred_solution":  top["amar_putusan"],
        "true_solution":  q.get("true_solution", "")
    })

df_out = pd.DataFrame(rows)

# ─── 5) Simpan hasil retrieval ─────────────────────────────────────
os.makedirs("data/results", exist_ok=True)
out_path = "data/results/stage3_retrieval.csv"
df_out.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"Saved Stage 3 retrieval results to {out_path}")

# Optional demo print
print(df_out.head())
