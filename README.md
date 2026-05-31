# E-Commerce Dashboard

Dashboard ini dibuat menggunakan Streamlit dengan data utama di `dashboard/all_data.csv`.

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

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

## Run Streamlit App

Jalankan dari root folder project:

```bash
streamlit run dashboard/dashboard.py
```

