# 💰 Prediksi Nilai Gadai Elektronik — Streamlit App

Aplikasi ini digunakan untuk memprediksi estimasi **nilai gadai barang elektronik** seperti HP, laptop, dan TV berdasarkan data historis. Model machine learning yang digunakan adalah **Random Forest Regressor**, dilengkapi preprocessing otomatis serta feature selection menggunakan **SelectKBest (Mutual Information Regression)**.

Antarmuka dibangun menggunakan **Streamlit** dengan tampilan modern berwarna putih–biru.

---

## 📌 Fitur Utama

- Pemilihan **jenis barang**
- Dropdown **tipe barang** yang otomatis terfilter sesuai jenis
- Input **tenor (hari)**
- Prediksi nilai gadai menggunakan model Random Forest yang telah dituning
- UI modern dengan custom CSS
- Penanganan error otomatis

---

## 🛠 Instalasi & Menjalankan Aplikasi

### 1 Buat virtual environment (opsional)

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2 Install dependency
```bash
pip install -r requirements.txt
```

### 3 Jalankan streamlit
```bash
streamlit run app.py
```

---

## ✨ Contoh Penggunaan

- Pilih jenis barang -> contoh: HP
- Pilih tipe HP -> contoh: OPPO A57
- Masukkan tenor (hari) -> contoh: 30
- Klik Prediksi Nilai Gadai

Aplikasi akan menampilkan estimasi, misalnya:
```bash
Rp 450.000
```

---

## 👨‍💻 Catatan Pengembang / Catatan Skripsi

**Update Terakhir (Arsitektur Database):**
Sistem ini telah diperbarui untuk menggunakan **SQLite** (`database_gadai.db`) secara penuh.
1. **File `options.json` sudah usang (Deprecated).** Seluruh referensi jenis dan tipe barang kini langsung ditarik (SELECT) dari tabel `master_barang`.
2. **Fitur Logging / Riwayat:** Setiap kali pengguna menekan tombol "Prediksi", hasilnya beserta `id_barang` (Foreign Key) akan tersimpan ke dalam tabel `riwayat_prediksi`.
3. **Database Viewer:** Terdapat menu tersembunyi (Expander) di bagian paling bawah antarmuka aplikasi untuk melihat langsung isi tabel riwayat, yang sudah di-JOIN dengan tabel `master_barang`. Sangat berguna untuk kebutuhan demonstrasi saat sidang Skripsi.

**Untuk Pengembangan Selanjutnya:**
* Jika ingin menambah data tipe barang baru, silakan gunakan tool database eksternal (seperti **DB Browser for SQLite** atau **VS Code SQLite Extension**) untuk menambahkan row langsung ke dalam tabel `master_barang`.
* Pastikan tidak menghapus file `.db` jika tidak ingin kehilangan riwayat transaksi prediksi yang sudah ada.