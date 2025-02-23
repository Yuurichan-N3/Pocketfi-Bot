## 🚀 PocketFi Bot

PocketFi Bot adalah skrip otomatisasi untuk mengelola aktivitas mining dan tugas harian di platform PocketFi. Skrip ini mendukung multi-akun, otomatisasi klaim mining, aktivasi boost harian, dan penyelesaian berbagai jenis tugas.

## ✨ Fitur

🧑‍🤖 Multi-akun: Mendukung banyak akun melalui file data.txt.

⛏️ Mining otomatis: Mengambil saldo dan kecepatan mining secara otomatis.

⚡ Klaim harian: Mengaktifkan boost harian untuk meningkatkan hasil mining.

✅ Tugas otomatis: Menyelesaikan misi harian, koneksi, dan tugas mitra secara otomatis.

⚙️ Pengaturan thread: Menggunakan thread pool untuk paralelisasi proses akun.

📊 Visualisasi data: Menampilkan hasil mining dalam tabel interaktif dengan Rich.


## 🛠️ Instalasi

1. Clone repositori ini (atau simpan skripnya):

```
git clone https://github.com/Yuurichan-N3/Pocketfi-Bot.git
cd Pocketfi-Bot
```

2. Buat virtual environment (opsional):

```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependensi:
```

pip install -r requirements.txt
```


## ⚙️ Konfigurasi

1. Buat file data.txt:
Masukkan data autentikasi dari PocketFi (misalnya token Telegram). Setiap baris adalah data untuk satu akun.

Contoh isi data.txt:

query=
user=


2. Atur jumlah thread:
Saat dijalankan, skrip akan meminta jumlah thread yang digunakan (1-50). Ini menentukan berapa banyak akun yang diproses secara paralel.



## ▶️ Penggunaan

Jalankan bot dengan perintah berikut:

```
python bot.py
```

🔸 Saat bot berjalan:

🟢 Mengambil data mining (saldo & kecepatan).

🔥 Mengaktifkan boost harian (jika belum dilakukan).

💰 Mengklaim hasil mining yang terkumpul.

🏁 Mengerjakan tugas otomatis (langganan, koneksi, trading).

⏳ Setelah selesai, bot akan menunggu 5 jam sebelum mengulangi proses.


## 🛑 Menghentikan bot

Tekan CTRL + C untuk menghentikan bot kapan saja.

## 📦 Dependensi

📩 requests — untuk HTTP requests ke API PocketFi.

📈 tqdm — untuk menampilkan progress bar saat countdown.

🖼️ rich — untuk logging yang lebih baik dan tabel interaktif.


Install semua dependensi dengan:

```
pip install -r requirements.txt
```

## ⚡ Catatan

📶 Pastikan koneksi internet stabil agar bot tidak terputus saat memproses data.

🚨 Jika ada kesalahan koneksi, bot akan mencatat log error dan melanjutkan ke akun berikutnya.


