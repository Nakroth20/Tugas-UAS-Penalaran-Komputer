import os
import json
import pandas as pd

# Import fungsi retrieve dari Tahap 3
from notebooks03_retrieval import retrieve

# 1) Siapkan folder output
os.makedirs("data/results", exist_ok=True)

# 2) Load queries.json
with open("data/eval/queries.json", "r", encoding="utf-8") as f:
    queries = json.load(f)

# 3) Untuk setiap query, ambil top-1 case
rows = []
for q in queries:
    # ambil id; fallback ke query_id jika perlu
    qid   = q.get("id") or q.get("query_id")
    text  = q["query"]
    true_ = q.get("true_solution", "")

    top   = retrieve(text, k=1)[0]
    rows.append({
        "query_id":       qid,
        "query_text":     text,
        "true_solution":  true_,
        "retrieved_case": top["case_id"],
        "pred_solution":  top["amar_putusan"]
    })

# 4) Simpan predictions.csv
df_pred = pd.DataFrame(rows)
outp = "data/results/predictions.csv"
df_pred.to_csv(outp, index=False, encoding="utf-8-sig")
print(f"[Stage 4] Saved predictions to {outp}")
