Laporan Proyek Case-Based Reasoning untuk Putusan Pengadilan
Deskripsi Proyek
Proyek ini bertujuan untuk mengimplementasikan sistem Case-Based Reasoning (CBR) yang digunakan untuk menganalisis dan mencari putusan pengadilan yang relevan berdasarkan putusan Mahkamah Agung Republik Indonesia. Sistem ini menerima input berupa query atau pertanyaan terkait dengan keputusan hukum, dan memberikan output berupa rekomendasi putusan yang paling relevan berdasarkan kemiripan dengan kasus-kasus yang ada dalam database.

Struktur Proyek
Pendahuluan

Menjelaskan latar belakang, permasalahan yang dihadapi, dan tujuan penerapan CBR dalam menganalisis putusan pengadilan.

Metodologi

Menjelaskan rincian proses 5 tahap CBR yang diterapkan dalam proyek ini, termasuk:

Membangun Case Base

Representasi Kasus

Retrieval Kasus

Reuse Solusi

Evaluasi

Implementasi

Menyajikan pipeline implementasi proyek yang meliputi pengunduhan data, preprocessing, pembentukan model TF-IDF, perhitungan cosine similarity, dan penerapan sistem.

Hasil dan Evaluasi

Menampilkan hasil evaluasi sistem berdasarkan metrik seperti accuracy, precision, recall, dan F1-score.

Tabel metrik evaluasi disertakan beserta analisis mengenai tantangan dan faktor-faktor yang mempengaruhi performa.

Diskusi

Menyediakan analisis kegagalan pada beberapa kasus yang tidak ditemukan, serta rekomendasi untuk memperbaiki dan meningkatkan akurasi model.

Kesimpulan

Menyimpulkan hasil yang didapat dari eksperimen dan hasil yang diharapkan di masa depan.

Metrik Evaluasi
Metrik yang digunakan untuk mengevaluasi sistem adalah:

Accuracy: Mengukur persentase kasus yang berhasil diambil dengan benar.

Precision: Mengukur persentase kasus yang relevan dari total hasil retrieval.

Recall: Mengukur persentase kasus relevan yang berhasil ditemukan dari keseluruhan kasus relevan.

F1-Score: Kombinasi dari precision dan recall untuk menilai keseimbangan antara keduanya.

Hasil Evaluasi:

Accuracy: 30.00%

Precision: 17.60%

Recall: 25.00%

F1-Score: 20.20%

Cara Penggunaan
1. Lingkungan Pengembangan
Sebelum memulai instalasi, disarankan untuk menggunakan virtual environment agar dependensi dapat terisolasi. Ikuti langkah-langkah di bawah ini untuk instalasi dan menjalankan proyek:

2. Instalasi Dependencies
Buat Virtual Environment (Opsional):

bash
Copy
Edit
# Membuat virtual environment
python -m venv cbr_env

# Mengaktifkan virtual environment
# Windows
cbr_env\Scripts\activate
# Linux/MacOS
source cbr_env/bin/activate
Install dependencies dengan file requirements.txt:

requirements.txt

txt
Copy
Edit
pandas==1.3.3
scikit-learn==0.24.2
python-docx==0.8.11
nltk==3.6.3
transformers==4.15.0
Untuk menginstal dependencies, jalankan perintah berikut:

bash
Copy
Edit
pip install -r requirements.txt
Jika Anda menggunakan Jupyter, Anda bisa menjalankan perintah berikut untuk instalasi:

bash
Copy
Edit
pip install notebook
3. Menjalankan Pipeline End-to-End
Setelah dependencies terpasang, Anda bisa mengikuti langkah-langkah berikut untuk menjalankan pipeline dari preprocessing hingga evaluasi:

Langkah 1: Persiapkan File dan Data
Pastikan file data berikut tersedia dalam folder yang sesuai:

cases.csv: Berisi metadata dan teks lengkap dari putusan-putusan pengadilan.

queries_with_true_case.json: Berisi query dan solusi yang diharapkan untuk evaluasi.

Letakkan file tersebut di lokasi berikut:

/data/processed/cases.csv

/data/queries_with_true_case.json

Langkah 2: Preprocessing dan Model Training
Berikut adalah cara melakukan preprocessing dan training model TF-IDF:

python
Copy
Edit
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
df_cases = pd.read_csv('/path/to/data/processed/cases.csv')
df_queries = pd.read_json('/path/to/data/queries_with_true_case.json')

# Preprocessing function for text cleaning
def preprocess_text(text):
    # Implement preprocessing like removing stopwords, punctuation, etc.
    return text.lower()  # simple example, extend as needed

# Apply preprocessing to the 'text_full' column of the cases
df_cases['text_clean'] = df_cases['text_full'].apply(preprocess_text)
Langkah 3: Training TF-IDF Model
Melakukan fit dan transform pada data teks menggunakan TF-IDF.

python
Copy
Edit
# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
X_tfidf = tfidf_vectorizer.fit_transform(df_cases['text_clean'])
Langkah 4: Retrieval dengan Cosine Similarity
python
Copy
Edit
from sklearn.metrics.pairwise import cosine_similarity

# Preprocess query
query = "membatalkan pemberhentian mahasiswa Arbi Muhammad Nur"
query_vector = tfidf_vectorizer.transform([preprocess_text(query)])

# Cosine similarity calculation
cosine_similarities = cosine_similarity(query_vector, X_tfidf)

# Get the most similar case
most_similar_case_idx = cosine_similarities.argmax()
retrieved_case = df_cases.iloc[most_similar_case_idx]
print(f"Most relevant case for query '{query}': {retrieved_case['text_full']}")
Langkah 5: Evaluasi dan Pengujian
Evaluasi hasil retrieval dengan metrik accuracy, precision, recall, dan F1-score.

python
Copy
Edit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Prepare true labels and predicted results for evaluation
true_labels = df_queries['true_solution']  # Based on the dataset structure
predicted_results = df_queries['retrieved_case'].apply(lambda x: x['solution'])  # Example access method

# Evaluate using sklearn's metrics
accuracy = accuracy_score(true_labels, predicted_results)
precision = precision_score(true_labels, predicted_results, average='micro')
recall = recall_score(true_labels, predicted_results, average='micro')
f1 = f1_score(true_labels, predicted_results, average='micro')

print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1-Score: {f1:.2%}")
Langkah 6: Simpan Hasil
Jika Anda ingin menyimpan hasil prediksi atau metrik evaluasi ke dalam file CSV atau Excel:

python
Copy
Edit
# Save results to CSV
df_results = pd.DataFrame({
    'query_id': df_queries['query_id'],
    'true_solution': true_labels,
    'retrieved_case': predicted_results
})
df_results.to_csv('/path/to/save/predictions.csv', index=False)
4. Menjalankan Skrip
Setelah menyiapkan semua file dan data, Anda dapat menjalankan pipeline menggunakan perintah berikut:

bash
Copy
Edit
# Mengaktifkan virtual environment (jika belum aktif)
source cbr_env/bin/activate  # Linux/MacOS
# cbr_env\Scripts\activate  # Windows

# Menjalankan Jupyter Notebook
jupyter notebook

# Atau menjalankan skrip Python langsung dari terminal
python3 cbr_pipeline.py
Kesimpulan
Dengan mengikuti langkah-langkah di atas, Anda dapat menjalankan pipeline end-to-end dari preprocessing hingga evaluasi menggunakan CBR untuk menganalisis putusan pengadilan. Proyek ini dapat dikembangkan lebih lanjut dengan menggunakan model berbasis embedding seperti IndoBERT untuk meningkatkan performa retrieval yang lebih akurat.
