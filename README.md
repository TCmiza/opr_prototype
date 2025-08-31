
# Sistem OPR – Prototype (Streamlit)

Prototipe aplikasi web untuk **auto jana One Page Report (OPR)**. Cikgu hanya isi borang, upload gambar, dan klik *Generate* – sistem akan hasilkan PDF A4 satu muka surat yang kemas.

## 🚀 Cara Jalankan (Tempatan)
1. Pastikan **Python 3.9+** terpasang.
2. Buka terminal, jalankan:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Aplikasi akan buka di browser (biasanya `http://localhost:8501`).

## ☁️ Deploy ke Streamlit Cloud (Percuma)
1. Buat repo GitHub dan upload semua fail dalam folder projek ini.
2. Pergi ke [streamlit.io/cloud](https://streamlit.io/cloud) → *Deploy an app* → sambungkan repo.
3. Set **Python version** (cth: 3.10), dan *Main file path* = `app.py`.
4. Klik **Deploy** – siap. Boleh guna di phone & laptop.

## 🧩 Ciri Utama
- Borang lengkap: tajuk, tarikh/masa, tempat, penganjur, sasaran, kehadiran, objektif, aktiviti, impak, cadangan.
- Upload logo sekolah (pilihan) + hingga 3 gambar program.
- PDF layout satu muka surat, kemas dan tersusun.
- Butang muat turun PDF + pratonton PDF terus dalam halaman.

## 🖼️ Tip Gambar
- Gambar melintang (landscape) akan muat lebih cantik dalam baris galeri.
- Saiz fail sederhana (di bawah 1 MB) memudahkan upload.

## ✏️ Ubah Suai Template
Reka bentuk PDF boleh diubah di `report_generator.py`:
- Warna tema (kod hex) – bar header, tajuk seksyen.
- Susun atur, fon, dan tajuk seksyen.

Kalau perlukan versi dengan **format mengikut template sekolah cikgu**, boleh beritahu – kita boleh sesuaikan posisi, logo tetap, dan gaya tulisan.

---

**Nota privasi:** Fail gambar tidak disimpan; hanya digunakan ketika penjanaan PDF lalu dipadam sementara.
