import tkinter as tk # Mengimpor modul tkinter untuk membuat GUI (Antarmuka Pengguna)
from tkinter import messagebox, simpledialog # Mengimpor kotak pesan dan dialog dari tkinter
import json # Mengimpor modul json untuk membaca file data JSON
import os # Mengimpor modul os untuk berinteraksi dengan sistem file
import random # Mengimpor modul random untuk mode kuis

# ==========================================
# 1. STRUKTUR DATA: TRIE (Untuk Autocomplete)
# ==========================================
class TrieNode: # Membuat kelas untuk setiap simpul (node) pada Trie
    def __init__(self): # Konstruktor untuk menginisialisasi node baru
        self.children = {} # Dictionary (Hash Table) untuk menyimpan huruf-huruf anak
        self.is_end_of_word = False # Boolean penanda apakah node ini adalah akhir dari sebuah kata

class Trie: # Membuat kelas Trie untuk menampung seluruh node
    def __init__(self): # Konstruktor Trie
        self.root = TrieNode() # Menginisialisasi akar (root) Trie sebagai TrieNode kosong

    def insert(self, word): # Fungsi untuk memasukkan kata ke dalam Trie
        node = self.root # Memulai dari akar (root)
        for char in word: # Melakukan iterasi untuk setiap huruf dalam kata
            if char not in node.children: # Jika huruf belum ada di anak-anak node
                node.children[char] = TrieNode() # Buat node baru untuk huruf tersebut
            node = node.children[char] # Pindah ke node anak tersebut
        node.is_end_of_word = True # Setelah semua huruf dimasukkan, tandai sebagai akhir kata

    def search_prefix(self, prefix): # Fungsi untuk mencari node akhir dari sebuah awalan (prefix)
        node = self.root # Memulai dari akar
        for char in prefix: # Iterasi setiap huruf dalam awalan
            if char not in node.children: # Jika huruf tidak ditemukan
                return None # Kembalikan None karena awalan tidak ada
            node = node.children[char] # Pindah ke anak node
        return node # Kembalikan node terakhir dari awalan tersebut

    def get_words_with_prefix(self, prefix): # Fungsi untuk mengambil semua kata dengan awalan tertentu
        node = self.search_prefix(prefix) # Mencari node awalan
        words = [] # List kosong untuk menyimpan daftar kata yang ditemukan
        if node: # Jika node awalan ditemukan
            self._dfs(node, prefix, words) # Panggil fungsi pencarian DFS (Depth First Search)
        return words # Kembalikan daftar kata

    def _dfs(self, node, current_word, words): # Fungsi rekursif DFS untuk menelusuri Trie
        if node.is_end_of_word: # Jika node ini adalah akhir kata
            words.append(current_word) # Tambahkan kata ke dalam list words
        for char, child_node in node.children.items(): # Iterasi semua anak dari node saat ini
            self._dfs(child_node, current_word + char, words) # Panggil DFS lagi dengan menambahkan huruf

# ==========================================
# 2. STRUKTUR DATA: DOUBLY LINKED LIST (Riwayat)
# ==========================================
class NodeDLL: # Kelas untuk simpul (node) pada Doubly Linked List
    def __init__(self, data): # Konstruktor node DLL
        self.data = data # Menyimpan data (berupa kata yang dicari)
        self.prev = None # Pointer untuk menunjuk ke node sebelumnya
        self.next = None # Pointer untuk menunjuk ke node selanjutnya

class DoublyLinkedList: # Kelas untuk Doubly Linked List itu sendiri
    def __init__(self): # Konstruktor DLL
        self.head = None # Pointer ke simpul pertama
        self.tail = None # Pointer ke simpul terakhir
        self.current = None # Pointer untuk menandai posisi saat ini (untuk Back/Forward)

    def add(self, data): # Fungsi menambahkan riwayat baru
        new_node = NodeDLL(data) # Membuat node baru
        if self.head is None: # Jika list masih kosong
            self.head = new_node # Node baru menjadi kepala (head)
            self.tail = new_node # Node baru menjadi ekor (tail)
            self.current = new_node # Posisi saat ini berada di node baru
        else: # Jika list tidak kosong
            new_node.prev = self.current # Node baru menunjuk ke node saat ini sebagai prev
            self.current.next = new_node # Node saat ini menunjuk ke node baru sebagai next
            self.tail = new_node # Ekor diperbarui menjadi node baru
            self.current = new_node # Posisi saat ini pindah ke node baru

    def go_back(self): # Fungsi untuk mundur satu langkah di riwayat (Back)
        if self.current and self.current.prev: # Jika ada posisi saat ini dan ada posisi sebelumnya
            self.current = self.current.prev # Pindah ke posisi sebelumnya
            return self.current.data # Kembalikan kata di posisi tersebut
        return None # Jika tidak bisa mundur, kembalikan None

    def go_forward(self): # Fungsi untuk maju satu langkah di riwayat (Forward)
        if self.current and self.current.next: # Jika ada posisi saat ini dan ada posisi selanjutnya
            self.current = self.current.next # Pindah ke posisi selanjutnya
            return self.current.data # Kembalikan kata di posisi tersebut
        return None # Jika tidak bisa maju, kembalikan None

# ==========================================
# 3. ALGORITMA LEVENSHTEIN (Fuzzy Search)
# ==========================================
def levenshtein_distance(s1, s2): # Fungsi untuk menghitung jarak perubahan antara dua kata
    if len(s1) < len(s2): # Jika s1 lebih pendek
        return levenshtein_distance(s2, s1) # Tukar posisi s1 dan s2 agar s1 selalu lebih panjang
    if len(s2) == 0: # Jika s2 kosong
        return len(s1) # Jaraknya adalah panjang s1 (harus menambah sebanyak panjang s1)
    
    previous_row = range(len(s2) + 1) # Inisialisasi baris pertama perhitungan
    for i, c1 in enumerate(s1): # Iterasi setiap karakter di kata pertama
        current_row = [i + 1] # Baris saat ini diawali dengan indeks i+1
        for j, c2 in enumerate(s2): # Iterasi setiap karakter di kata kedua
            insertions = previous_row[j + 1] + 1 # Hitung biaya jika menambah (insertion)
            deletions = current_row[j] + 1 # Hitung biaya jika menghapus (deletion)
            substitutions = previous_row[j] + (c1 != c2) # Hitung biaya jika mengganti (substitution)
            current_row.append(min(insertions, deletions, substitutions)) # Pilih biaya terkecil
        previous_row = current_row # Pindah ke baris berikutnya
    return previous_row[-1] # Kembalikan nilai di pojok kanan bawah (jarak total)

# ==========================================
# 4. KELAS APLIKASI GUI UTAMA
# ==========================================
class KamusApp: # Kelas utama untuk aplikasi
    def __init__(self, root): # Konstruktor dengan parameter root (jendela Tkinter)
        self.root = root # Menyimpan referensi jendela utama
        self.root.title("Kamus Multi Guna") # Memberi judul pada jendela aplikasi
        self.root.geometry("600x550") # Mengatur ukuran jendela menjadi 600x550 pixel
        
        self.hash_table = {} # Inisialisasi Hash Table menggunakan dictionary bawaan Python
        self.trie = Trie() # Menginisialisasi objek Trie untuk autocomplete
        self.history = DoublyLinkedList() # Menginisialisasi objek Doubly Linked List untuk riwayat
        self.favorites = set() # Menginisialisasi Set untuk menyimpan kata favorit (agar tidak ganda)
        
        self.load_data() # Memanggil fungsi untuk memuat data JSON ke struktur data
        self.create_widgets() # Memanggil fungsi untuk membuat elemen-elemen GUI
        
    def load_data(self): # Fungsi membaca dan memasukkan data kamus
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Mendapatkan folder tempat script ini berada
        path_kamus = os.path.join(script_dir, "jeson", "kamus.json") # Menentukan path file kamus baru secara absolut
        if os.path.exists(path_kamus): # Mengecek apakah file tersebut ada
            with open(path_kamus, 'r', encoding='utf-8') as f: # Membuka file untuk dibaca
                data = json.load(f) # Membaca file JSON
                for item in data: # Iterasi setiap entri di dalam list JSON
                    indonesia = item.get("indonesia", "") # Mengambil kata bahasa Indonesia
                    inggris = item.get("inggris", "") # Mengambil kata bahasa Inggris
                    sunda = item.get("sunda", "") # Mengambil kata bahasa Sunda
                    sinonim = ", ".join(item.get("sinonim", [])) # Menggabungkan array sinonim menjadi string
                    antonim = ", ".join(item.get("antonim", [])) # Menggabungkan array antonim menjadi string
                    
                    # Format teks terjemahan yang akan ditampilkan
                    arti_teks = f"\n- Indonesia: {indonesia}\n- Inggris: {inggris}\n- Sunda: {sunda}"
                    if sinonim: arti_teks += f"\n- Sinonim: {sinonim}"
                    if antonim: arti_teks += f"\n- Antonim: {antonim}"
                    
                    # Fungsi internal untuk menambahkan kata ke struktur data
                    def tambah_kata(kata):
                        if kata: # Jika kata tidak kosong
                            kata_lower = kata.lower() # Ubah ke huruf kecil
                            self.hash_table[kata_lower] = arti_teks # Simpan teks arti ke Hash Table (Dictionary)
                            self.trie.insert(kata_lower) # Masukkan kata ke Trie untuk Autocomplete
                            
                    # Menambahkan semua bahasa agar bisa dicari dari bahasa mana pun
                    tambah_kata(indonesia)
                    tambah_kata(inggris)
                    tambah_kata(sunda)
                    
    def create_widgets(self): # Fungsi untuk mengatur tampilan GUI
        search_frame = tk.Frame(self.root) # Membuat sebuah frame penampung untuk area pencarian
        search_frame.pack(pady=10) # Menempatkan frame dengan padding (jarak) atas-bawah 10
        
        tk.Label(search_frame, text="Masukkan Kata:").pack(side=tk.LEFT) # Menambahkan label teks
        
        self.entry_var = tk.StringVar() # Variabel penampung teks untuk entry pencarian
        self.entry_var.trace_add("write", self.on_typing) # Memicu fungsi on_typing setiap kali ada teks diketik
        
        self.entry = tk.Entry(search_frame, textvariable=self.entry_var, width=35) # Membuat input teks (Entry)
        self.entry.pack(side=tk.LEFT, padx=5) # Menempatkan input di sebelah kiri dengan padding samping 5
        
        tk.Button(search_frame, text="Cari", command=self.search_word).pack(side=tk.LEFT) # Membuat tombol Cari
        
        self.autocomplete_list = tk.Listbox(self.root, height=5, width=50) # Membuat kotak daftar (Listbox) untuk Autocomplete
        self.autocomplete_list.pack() # Menempatkan Listbox ke dalam jendela
        self.autocomplete_list.bind("<<ListboxSelect>>", self.on_autocomplete_select) # Jika item diklik, jalankan fungsi
        
        nav_frame = tk.Frame(self.root) # Membuat frame untuk tombol navigasi
        nav_frame.pack(pady=10) # Menempatkan frame dengan padding
        
        tk.Button(nav_frame, text="< Back", command=self.go_back).pack(side=tk.LEFT, padx=5) # Membuat tombol Back
        tk.Button(nav_frame, text="Forward >", command=self.go_forward).pack(side=tk.LEFT, padx=5) # Membuat tombol Forward
        tk.Button(nav_frame, text="Tambah Favorit", command=self.add_favorite).pack(side=tk.LEFT, padx=5) # Tombol Tambah Favorit
        
        menu_frame = tk.Frame(self.root) # Membuat frame untuk menu tambahan
        menu_frame.pack(pady=5) # Menempatkan frame dengan padding
        
        tk.Button(menu_frame, text="Daftar Favorit", command=self.show_favorites).pack(side=tk.LEFT, padx=5) # Tombol Lihat Favorit
        tk.Button(menu_frame, text="Mode Kuis", command=self.quiz_mode).pack(side=tk.LEFT, padx=5) # Tombol untuk Kuis
        
        self.result_text = tk.Text(self.root, height=12, width=65, state=tk.DISABLED) # Membuat area Teks hasil (Text)
        self.result_text.pack(pady=10) # Menempatkan area Teks dengan padding
        
    def on_typing(self, *args): # Fungsi ini dijalankan saat user mengetik huruf
        prefix = self.entry_var.get().lower() # Mengambil huruf/kata yang sedang diketik
        self.autocomplete_list.delete(0, tk.END) # Mengosongkan daftar saran (autocomplete) sebelumnya
        if prefix: # Jika kotak pencarian tidak kosong
            words = self.trie.get_words_with_prefix(prefix) # Cari di Trie semua kata yang memiliki awalan ini
            for w in words[:6]: # Ambil maksimal 6 kata pertama saja
                self.autocomplete_list.insert(tk.END, w) # Masukkan kata tersebut ke Listbox untuk ditampilkan
                
    def on_autocomplete_select(self, event): # Fungsi ini jalan jika user mengklik salah satu saran Autocomplete
        selection = event.widget.curselection() # Cek baris ke berapa yang dipilih oleh user
        if selection: # Jika ada baris yang dipilih
            word = event.widget.get(selection[0]) # Ambil teks dari baris tersebut
            self.entry_var.set(word) # Isi teks tersebut ke kotak input pencarian (Entry)
            self.search_word() # Langsung lakukan proses pencarian

    def display_result(self, text): # Fungsi pembantu untuk menampilkan pesan di kotak Hasil (Text)
        self.result_text.config(state=tk.NORMAL) # Buka kunci edit Text agar bisa disisipi teks
        self.result_text.delete(1.0, tk.END) # Hapus isi yang sudah ada sebelumnya
        self.result_text.insert(tk.END, text) # Tulis/sisipkan teks yang baru
        self.result_text.config(state=tk.DISABLED) # Kunci kembali edit Text agar teks tidak bisa diubah user
            
    def search_word(self, word_to_search=None): # Fungsi utama mencari arti kata
        word = word_to_search or self.entry_var.get().lower().strip() # Mengambil kata, membersihkan spasi depan/belakang
        if not word: # Jika kosong, batalkan
            return # Keluar fungsi
            
        if word in self.hash_table: # 1. Cari kata langsung di Hash Table (Pencarian O(1))
            arti = self.hash_table[word] # Jika ada, ambil artinya
            self.display_result(f"Kata: {word}\nArti: {arti}") # Tampilkan kata dan artinya
            if not word_to_search: # Jika dipanggil dari tombol cari (bukan dari Back/Forward)
                self.history.add(word) # Masukkan kata tersebut ke Doubly Linked List sebagai Riwayat
        else:
            self.display_result(f"Kata '{word}' tidak ditemukan.\nMencari saran...") # Info bahwa akan mencari saran
            self.root.update() # Memaksa update tampilan GUI
            
            # 2. Fitur Typo / Fuzzy Search dengan Algoritma Levenshtein
            closest_word = None # Variabel penyimpan kata paling mendekati
            min_dist = float('inf') # Set batas awal jarak ke tak terhingga (infinity)
            
            for key in self.hash_table.keys(): # Looping ke seluruh kata di dalam Hash Table
                if abs(len(key) - len(word)) <= 2: # Untuk menghemat performa, hanya cek panjang kata yang mirip (selisih maksimal 2 huruf)
                    dist = levenshtein_distance(word, key) # Menghitung jarak Levenshtein antara input dan kata di tabel
                    if dist < min_dist: # Jika jaraknya lebih kecil dari yang tersimpan
                        min_dist = dist # Update jarak terdekat yang baru
                        closest_word = key # Update kata yang paling mendekati
                        
            if closest_word and min_dist <= 2: # Jika ada kata terdekat dan jarak perubahannya wajar (maksimal 2 perubahan)
                arti = self.hash_table[closest_word] # Ambil arti dari kata saran tersebut
                self.display_result(f"Kata '{word}' tidak ditemukan.\n\nMungkin maksud Anda: '{closest_word}' ?\nArti: {arti}") # Tampilkan saran
            else:
                self.display_result(f"Kata '{word}' tidak ditemukan dan tidak ada saran kata yang cocok.") # Info jika gagal menebak typo

    def go_back(self): # Fungsi saat tombol < Back diklik
        prev_word = self.history.go_back() # Mundur di Doubly Linked List dan ambil datanya
        if prev_word: # Jika berhasil (ada riwayat sebelumnya)
            self.entry_var.set(prev_word) # Ubah isi kotak pencarian jadi kata riwayat tersebut
            self.search_word(prev_word) # Langsung jalankan pencarian untuk menampilkannya
            
    def go_forward(self): # Fungsi saat tombol Forward > diklik
        next_word = self.history.go_forward() # Maju di Doubly Linked List dan ambil datanya
        if next_word: # Jika berhasil
            self.entry_var.set(next_word) # Ubah isi kotak pencarian
            self.search_word(next_word) # Langsung jalankan pencarian
            
    def add_favorite(self): # Fungsi menyimpan daftar Favorit
        word = self.entry_var.get().lower().strip() # Mengambil kata dari kotak input
        if word in self.hash_table: # Memastikan bahwa kata tersebut valid dan ada artinya
            self.favorites.add(word) # Masukkan kata tersebut ke objek set `favorites`
            messagebox.showinfo("Berhasil", f"'{word}' berhasil ditambahkan ke Favorit.") # Memunculkan pop-up pemberitahuan
        else:
            messagebox.showwarning("Gagal", "Silakan cari kata yang valid terlebih dahulu.") # Pop-up jika kata tidak valid
            
    def show_favorites(self): # Fungsi untuk melihat daftar kata Favorit
        if not self.favorites: # Mengecek jika himpunan favorites masih kosong
            messagebox.showinfo("Daftar Favorit", "Belum ada kata favorit yang disimpan.") # Pop-up jika kosong
            return # Keluar dari fungsi
        fav_list = "\n".join(self.favorites) # Menggabungkan semua kata favorit dengan baris baru (Enter)
        messagebox.showinfo("Daftar Favorit", fav_list) # Memunculkan pop-up berisi daftar favorit
        
    def quiz_mode(self): # Fungsi sederhana untuk Mode Kuis
        if not self.hash_table: # Jika hash table belum ada data (batal)
            return # Keluar dari fungsi
        word = random.choice(list(self.hash_table.keys())) # Mengacak satu kata dari kumpulan kata di Hash Table
        arti = self.hash_table[word] # Mengambil arti sebenarnya dari kata acak tersebut
        answer = simpledialog.askstring("Kuis", f"Apa terjemahan dari kata: '{word}'?") # Meminta jawaban user menggunakan Pop Up input
        if answer: # Jika user mengisi jawaban dan menekan OK
            messagebox.showinfo("Hasil Kuis", f"Jawaban Anda: {answer}\n\nArti Sebenarnya: {arti}") # Menampilkan perbandingan jawaban user dengan hasil asli

if __name__ == "__main__": # Bagian utama saat script dijalankan (entry point)
    root = tk.Tk() # Memulai jendela utama antarmuka tkinter
    app = KamusApp(root) # Memanggil (inisialisasi) kelas KamusApp dengan root sebagai parameter
    root.mainloop() # Memutar infinite loop GUI agar aplikasi tidak langsung tertutup
