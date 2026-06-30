# Alur Sistem Kamus Multi Guna (Terintegrasi Struktur Data)

## 📁 Arsitektur Proyek
Aplikasi ini dikembangkan dengan arsitektur modular yang memisahkan GUI dengan logika algoritma:
- **`Main.py`** : Mengelola antarmuka grafis (GUI) Tkinter dan interaksi pengguna.
- **`dataset/kamus.json`** : Basis data utama berformat JSON (Indonesia, Inggris, Sunda, Sinonim, Antonim).
- **`modules/`** : Kumpulan kelas struktur data & algoritma.
  - `Trie.py` *(Trie Tree)*
  - `HashTable.py` *(Custom Hash Table dengan Chaining)*
  - `DoublyLinkedList.py` *(Doubly Linked List)*
  - `FuzzySearch.py` *(Algoritma Levenshtein Distance)*

---

## 🔄 Alur Kerja Aplikasi

**1. Tahap Inisialisasi (Startup)**
- Aplikasi dijalankan melalui `Main.py`.
- Sistem membaca dan memuat *dataset* dari `dataset/kamus.json`.
- Seluruh kosa kata dipetakan ke dalam struktur data **Hash Table** untuk akses berkecepatan $O(1)$, dan dimasukkan ke dalam struktur **Trie** untuk keperluan *autocomplete*.

**2. Fitur Pencarian & Autocomplete**
- Pengguna mengetik kata pada kolom pencarian.
- Secara *real-time*, struktur data **Trie** akan memunculkan daftar saran kata (maksimal 6) yang berawalan sesuai ketikan.

**3. Proses Eksekusi Pencarian (Search)**
- Saat tombol **Cari** (atau *Enter*) ditekan:
  - **Ditemukan:** Sistem mengambil terjemahan, sinonim, dan antonim secara instan $O(1)$ dari **Hash Table**.
  - **Tidak Ditemukan:** Algoritma **Fuzzy Search (Levenshtein Distance)** akan dipanggil untuk mengalkulasi jarak *typo*. Aplikasi lalu menampilkan rekomendasi kata terdekat beserta artinya.
- Kata yang baru dicari akan ditambahkan secara dinamis ke dalam **Doubly Linked List** sebagai Riwayat.

**4. Navigasi & Manajemen Data**
- **Navigasi Riwayat:** Pengguna dapat menekan tombol `< Back` atau `Forward >` untuk berpindah ke hasil pencarian sebelumnya/selanjutnya berkat penunjuk arah (*pointer*) ganda di dalam **Doubly Linked List**.
- **Daftar Favorit:** Pengguna dapat mengeklik "⭐ Favorit" untuk menyimpan kosa kata ke dalam struktur set memori.
- **Tabel Rekap:** Menu "📋 Daftar" (Favorit) dan "🕓 Riwayat" (Pencarian) menampilkan rangkuman kata dalam antarmuka tabular.

**5. Mode Kuis Interaktif (Quiz)**
- Pengguna mengeklik menu "🎮 Kuis" untuk menguji wawasan kosa kata secara acak.
- Terdapat pilihan alur soal (Misal: Indonesia → Inggris).
- Skor akan disimpan secara berkelanjutan dan dapat dilihat melalui menu khusus "Riwayat Kuis".

**6. Keluar / Penutupan (End)**
- Saat jendela aplikasi ditutup, sesi pada memori akan dihapus dan program berakhir.
