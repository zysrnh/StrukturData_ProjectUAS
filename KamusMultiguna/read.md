Alur Kamus Multi Guna (Versi Lengkap dengan Struktur Data)

1. Jalankan Program / Start.
2. Sistem memuat (load) data kamus (Inggris-Indonesia & Sunda-Indonesia) ke dalam struktur data Hash Table dan Trie.
3. Tampilkan Menu Utama Aplikasi.
4. Pilih Menu (Pencarian Kamus / Daftar Favorit / Mode Kuis).
5. Masukkan Kata yang ingin dicari:
   - Saat user mengetik, struktur Trie bekerja memunculkan saran kata (Autocomplete).
6. Proses Pencarian (Menekan tombol Cari):
   - Hash Table akan mencari arti kata tersebut.
   - Jika ditemukan: Tampilkan Hasil Pencarian / Terjemahan.
   - Jika tidak ditemukan: Algoritma Levenshtein berjalan untuk mengecek typo, lalu menampilkan saran kata terdekat (Fuzzy Search).
7. Simpan Riwayat Pencarian:
   - Kata yang berhasil dicari otomatis dimasukkan ke dalam Doubly Linked List sebagai riwayat (History).
8. Navigasi:
   - User bisa menekan tombol '< Back' atau 'Forward >' untuk melihat kata yang dicari sebelumnya/selanjutnya (berdasarkan Doubly Linked List).
   - User bisa menyimpan kata tersebut ke Daftar Favorit.
9. Kembali ke Menu / Keluar (End).
