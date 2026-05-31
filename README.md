# E-Commerce Dashboard 2017

## Deskripsi Proyek

Proyek ini merupakan salah satu tugas submission dalam program Coding Camp 2026 powered by DBS Foundation x Dicoding. Proyek ini berfokus pada analisis data E-Commerce pada tahun 2017 dan menjawab tiga pertanyaan bisnis utama yaitu:
1. Bagaimana tren penjualan secara bulanan (Month-over-Month) sepanjang tahun 2017?
2. Bagaimana tingkat kepuasan pelanggan terhadap produk sepanjang tahun 2017?
3. Bagaimana pengaruh faktor operasional transaksi terhadap kepuasan pelanggan sepanjang tahun 2017?

Dashboard ini dibuat menggunakan Streamlit dengan data utama di `dashboard/all_data.csv`.
Jika notebook.ipnyb tidak bisa dibuka silakan cek Google Colab berikut: https://colab.research.google.com/drive/1RBNc_KDfPrfWoTOB2T5UspSg5wGrQGXr 

## Cara Menjalankan Proyek di Lokal
### Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal

Jika folder project sudah ada (seperti proyek ini), langsung masuk ke folder project lalu jalankan:

```bash
pipenv install
pipenv shell
pip install -r requirements.txt
```

Jika mulai dari nol, bisa gunakan langkah berikut:

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Run Streamlit App
Jalankan dari root folder project:

```bash
streamlit run dashboard/dashboard.py
```
##Insight
- Conclution pertanyaan 1: Penjualan sepanjang 2017 menunjukkan tren pertumbuhan bulanan yang positif, dengan performa terendah di awal tahun dan puncak penjualan terjadi pada November 2017. Hal ini menunjukkan adanya peningkatan permintaan yang konsisten sepanjang tahun, terutama menjelang akhir tahun.
- Conclution pertanyaan 2: Meskipun mayoritas pelanggan masih memberikan ulasan positif sepanjang 2017, rata-rata tingkat kepuasan menunjukkan tren penurunan secara bertahap. Hal ini mengindikasikan bahwa peningkatan volume transaksi belum sepenuhnya diimbangi dengan kualitas pengalaman pelanggan yang konsisten.
- Conclution pertanyaan 3: Dari seluruh faktor operasional yang dianalisis, waktu pengiriman merupakan faktor yang paling berpengaruh terhadap kepuasan pelanggan. Semakin lama waktu pengiriman, semakin rendah tingkat kepuasan pelanggan, sehingga optimasi proses pengiriman menjadi prioritas utama untuk meningkatkan customer experience.

