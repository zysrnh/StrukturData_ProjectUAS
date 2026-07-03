# Alur Sistem Kamus Multi Guna (Terintegrasi Struktur Data)

## 📁 Arsitektur Proyek
Aplikasi ini dikembangkan dengan arsitektur modular yang memisahkan antarmuka pengguna (GUI) dengan logika algoritma. Struktur direktori telah disesuaikan agar lebih profesional:
- **`main.py`** : Mengelola antarmuka grafis (GUI) Tkinter dan interaksi pengguna.
- **`dataset/kamus.json`** : Basis data utama berformat JSON yang berisi kosa kata (Indonesia, Inggris, Sunda, Sinonim, Antonim).
- **`modules/`** : Kumpulan kelas modul struktur data & algoritma.
  - `Trie.py` *(Trie Tree untuk Autocomplete)*
  - `HashTable.py` *(Custom Hash Table dengan Chaining untuk pencarian O(1))*
  - `DoublyLinkedList.py` *(Doubly Linked List untuk riwayat navigasi)*
  - `FuzzySearch.py` *(Algoritma Levenshtein Distance untuk koreksi salah ketik/typo)*

---

## 🎨 Antarmuka Pengguna (UI/UX)
- Aplikasi menerapkan palet warna "Kalem" (*muted steel-blue*) yang profesional dan modern (`#f0f2f5`, `#1e3a5f`, `#2563eb`).
- Menggunakan tipografi *Rich Text* pada hasil pencarian agar informasi (kata, arti, sinonim, antonim) lebih terstruktur dan mudah dibaca.
- Antarmuka mengandalkan elemen UI berbasis teks (*text-based UI elements*) yang bersih (tanpa *icon* berlebihan) agar terlihat elegan dan rapi.

---

## 🔄 Alur Kerja Aplikasi

**1. Tahap Inisialisasi (Startup)**
- Aplikasi dijalankan melalui `main.py`.
- Sistem memuat basis data dari `dataset/kamus.json`. Seluruh kosa kata dipetakan ke dalam struktur **Hash Table** dan dimasukkan ke dalam struktur **Trie**.
- Layar akan menampilkan **Halaman Selamat Datang (Welcome Screen)**. Pengguna dapat mengeklik "Mulai Belajar" untuk masuk ke antarmuka utama.

**2. Fitur Pencarian & Autocomplete (Trie)**
- Saat pengguna mengetik kata pada kolom pencarian, struktur **Trie** secara *real-time* akan memunculkan daftar saran kata (maksimal 6) yang berawalan sesuai huruf yang diketik.

**3. Proses Eksekusi Pencarian (Hash Table & Fuzzy Search)**
- Saat tombol **Cari** (atau *Enter*) ditekan:
  - **Ditemukan:** Sistem memanggil **Hash Table** untuk mengambil terjemahan, sinonim, dan antonim secara instan ($O(1)$).
  - **Tidak Ditemukan:** Algoritma **Fuzzy Search (Levenshtein Distance)** akan dipanggil untuk mengalkulasi jarak *typo*. Sistem akan memberikan rekomendasi maksimal 4 kata terdekat beserta artinya.
- Kata yang sukses dicari akan ditambahkan ke ujung **Doubly Linked List** (Riwayat).

**4. Navigasi & Manajemen Data (Doubly Linked List & Set)**
- **Navigasi Riwayat:** Menggunakan pointer di **Doubly Linked List**, pengguna dapat menekan tombol `< Back` atau `Forward >` untuk mundur/maju menelusuri riwayat kata yang pernah dicari.
- **Daftar Favorit:** Pengguna dapat menyimpan kata penting dengan mengeklik tombol "Favorit". Data akan disimpan dalam struktur `set()` agar terhindar dari duplikasi.
- **Tabel Rekap:** Melalui menu "Daftar" dan "Riwayat", pengguna bisa melihat rangkuman kata favorit atau riwayat pencarian dalam bentuk antarmuka tabel (`Treeview`).

**5. Mode Kuis Interaktif**
- Menu **Kuis** digunakan untuk menguji kemampuan kosa kata secara acak (Misal: Indonesia → Inggris, Sunda → Indonesia, dsb.).
- Sesi kuis mencatat statistik jawaban benar/salah. Hasil akhir berupa skor, persentase, dan predikat keberhasilan akan disimpan ke dalam **Riwayat Kuis**.

**6. Keluar / Penutupan**
- Saat jendela ditutup, memori sesi (riwayat, favorit sementara) akan dilepas, dan program berakhir.
