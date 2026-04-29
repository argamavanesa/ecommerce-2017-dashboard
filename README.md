# E-Commerce Dashboard

Dashboard ini dibuat dengan Streamlit dan mengambil data dari file `dashboard/all_data.csv`.

## Prasyarat

Pastikan sudah ada:

- Python 3.10+ terinstal
- `pip` tersedia di terminal

## Cara Install Dependency

1. Buka terminal atau command prompt di device.
2. Masuk ke folder project ini dengan perintah `cd` ke lokasi folder `submission`.
3. Jalankan perintah berikut untuk memasang dependency:

```powershell
pip install -r requirements.txt
```

Jika memakai virtual environment, aktifkan environment terlebih dahulu sebelum menjalankan perintah di atas.

## Cara Menjalankan Dashboard

Setelah dependency terpasang, jalankan Streamlit dari folder project yang sama:

```powershell
streamlit run dashboard\dashboard.py
```

Jika kamu berada di macOS atau Linux, gunakan separator folder `/` bila diperlukan, misalnya `dashboard/dashboard.py`.

Kalau file dashboard tidak ada di folder utama project kamu, sesuaikan path-nya dengan lokasi file `dashboard.py` yang kamu pakai.

## Cara Menghentikan Dashboard

Tekan:

```powershell
Ctrl + C
```

di terminal yang sedang menjalankan Streamlit.

