# ☕ Dashboard Sebaran Café Jawa Barat

Dashboard ini merupakan aplikasi berbasis **Streamlit** untuk memvisualisasikan sebaran lokasi café di wilayah **Jawa Barat** menggunakan peta interaktif dan grafik statistik.  
Data lokasi café ditampilkan berdasarkan koordinat geografis (latitude & longitude) yang telah melalui proses **reverse geocoding**.

---

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk:
- Menampilkan sebaran lokasi café secara visual dalam bentuk peta
- Mengelompokkan jumlah lokasi café berdasarkan **wilayah**
- Menyediakan ringkasan statistik yang mudah dipahami
- Membersihkan data dengan menghilangkan lokasi tanpa alamat yang valid

---

## 🧩 Fitur Utama

- 📍 **Peta Interaktif**
  - Menggunakan **Folium**
  - Marker menampilkan nama café dan alamat
- 📊 **Grafik Bar**
  - Menampilkan jumlah lokasi café per wilayah
- 📋 **Tabel Data**
  - Menampilkan dataset café yang telah difilter
- 📁 **Upload CSV**
  - Pengguna dapat mengunggah dataset sendiri

---

## 🗂 Struktur Data CSV

Dataset yang digunakan harus memiliki kolom berikut:

| Nama Kolom     | Keterangan                          |
|---------------|-------------------------------------|
| `nama`        | Nama café                           |
| `lat`         | Latitude lokasi                     |
| `lon`         | Longitude lokasi                    |
| `wilayah`     | Wilayah / kota                      |
| `alamat_asli` | Alamat hasil reverse geocoding      |

---

## 🔄 Alur Pengolahan Data

1. Dataset café dibaca dari file CSV
2. Proses **reverse geocoding** dilakukan menggunakan:
   - OpenStreetMap Nominatim
   - Library `geopy`
3. Data yang **tidak memiliki alamat valid** dihapus
4. Data bersih digunakan untuk:
   - Visualisasi peta
   - Grafik jumlah lokasi per wilayah
   - Tabel dataset

---

## 🛠 Teknologi yang Digunakan

- **Python**
- **Streamlit** – antarmuka aplikasi
- **Pandas** – pengolahan data
- **Folium** – peta interaktif
- **Altair** – visualisasi grafik
- **Geopy (Nominatim)** – reverse geocoding
- **OpenStreetMap** – sumber data alamat

---

## ▶️ Cara Menjalankan Aplikasi

1. Install dependensi:
   ```bash
   pip install streamlit pandas folium geopy altair streamlit-folium
  Atau
  ```bash
   pip install requirements.txt
