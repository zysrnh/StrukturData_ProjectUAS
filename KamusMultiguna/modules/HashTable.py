# ============================================================
# MODUL 5: STRUKTUR DATA HASH TABLE
# Digunakan untuk mencari arti kata dengan kompleksitas waktu O(1)
# ============================================================

class HashNode: # Kelas node untuk rantai hash (linked list dalam slot hash)
    def __init__(self, key, value): # Konstruktor HashNode
        self.key = key   # Kunci utama (kata yang dicari)
        self.value = value # Nilai associatif (arti kata)
        self.next = None   # Pointer ke node berikutnya dalam chain

class HashTable: # Kelas wadah utama hash table
    def __init__(self, capacity=1000): # Konstruktor HashTable
        self.capacity = capacity     # Kapasitas maksimal slot tabel (default 1000)
        self.size = 0                # Jumlah elemen yang saat ini tersimpan
        self.table = [None] * self.capacity # Array tabel hash diisi None pada awalnya

    def _hash(self, key): # Fungsi internal untuk menghitung nilai hash dari string
        hash_val = 0                 # Nilai awal hash
        for char in key:             # Iterasi setiap karakter pada kunci
            hash_val = (hash_val * 31 + ord(char)) % self.capacity # Hitung nilai hash (Rumus polinomial sederhana)
        return hash_val              # Kembalikan indeks array
        
    def set(self, key, value): # Fungsi untuk menyimpan/memperbarui data
        index = self._hash(key)      # Dapatkan indeks dari fungsi hash
        
        if self.table[index] is None: # Jika slot pada indeks ini kosong
            self.table[index] = HashNode(key, value) # Buat node pertama di slot ini
            self.size += 1           # Tambah ukuran tabel
            return
            
        current = self.table[index]  # Jika sudah ada node (terjadi collision/tabrakan)
        while current:               # Telusuri linked list pada slot ini
            if current.key == key:   # Jika kunci sudah ada
                current.value = value # Perbarui nilainya
                return
            if current.next is None: # Jika ini node terakhir
                break
            current = current.next   # Lanjut ke node berikutnya
            
        current.next = HashNode(key, value) # Tambahkan node baru di akhir rantai
        self.size += 1               # Tambah ukuran tabel

    def get(self, key, default=None): # Fungsi untuk mengambil nilai berdasarkan kunci
        index = self._hash(key)       # Dapatkan indeks dari kunci
        current = self.table[index]   # Ambil node pertama di slot ini
        
        while current:                # Telusuri rantai node
            if current.key == key:    # Jika kunci cocok
                return current.value  # Kembalikan arti/nilainya
            current = current.next    # Lanjut periksa node berikutnya
            
        return default                # Jika tidak ditemukan, kembalikan nilai default

    def contains(self, key): # Cek apakah kunci ada dalam tabel
        return self.get(key) is not None # Bernilai True jika tidak mengembalikan None

    def keys(self): # Ambil semua kunci yang tersimpan
        keys_list = []                # List penampung kunci
        for i in range(self.capacity): # Iterasi seluruh slot tabel
            current = self.table[i]   # Ambil node pada slot
            while current:            # Telusuri setiap rantai node
                keys_list.append(current.key) # Simpan kuncinya
                current = current.next # Lanjut ke node berikutnya
        return keys_list              # Kembalikan daftar semua kunci
