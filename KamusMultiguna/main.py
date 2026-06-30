# Mengimpor modul tkinter untuk membuat GUI (Antarmuka Pengguna)
import tkinter as tk
# Mengimpor kotak pesan dan dialog dari tkinter
from tkinter import messagebox, simpledialog
import json  # Mengimpor modul json untuk membaca file data JSON
import os  # Mengimpor modul os untuk berinteraksi dengan sistem file
import random  # Mengimpor modul random untuk mode kuis
import difflib  # Untuk fallback fuzzy matching

# ==========================================
# 1. STRUKTUR DATA: TRIE (Untuk Autocomplete)
# ==========================================


class TrieNode:  # Membuat kelas untuk setiap simpul (node) pada Trie
    def __init__(self):  # Konstruktor untuk menginisialisasi node baru
        # Dictionary (Hash Table) untuk menyimpan huruf-huruf anak
        self.children = {}
        # Boolean penanda apakah node ini adalah akhir dari sebuah kata
        self.is_end_of_word = False


class Trie:  # Membuat kelas Trie untuk menampung seluruh node
    def __init__(self):  # Konstruktor Trie
        self.root = TrieNode()  # Menginisialisasi akar (root) Trie sebagai TrieNode kosong

    def insert(self, word):  # Fungsi untuk memasukkan kata ke dalam Trie
        node = self.root  # Memulai dari akar (root)
        for char in word:  # Melakukan iterasi untuk setiap huruf dalam kata
            if char not in node.children:  # Jika huruf belum ada di anak-anak node
                # Buat node baru untuk huruf tersebut
                node.children[char] = TrieNode()
            node = node.children[char]  # Pindah ke node anak tersebut
        node.is_end_of_word = True  # Setelah semua huruf dimasukkan, tandai sebagai akhir kata

    # Fungsi untuk mencari node akhir dari sebuah awalan (prefix)
    def search_prefix(self, prefix):
        node = self.root  # Memulai dari akar
        for char in prefix:  # Iterasi setiap huruf dalam awalan
            if char not in node.children:  # Jika huruf tidak ditemukan
                return None  # Kembalikan None karena awalan tidak ada
            node = node.children[char]  # Pindah ke anak node
        return node  # Kembalikan node terakhir dari awalan tersebut

    # Fungsi untuk mengambil semua kata dengan awalan tertentu
    def get_words_with_prefix(self, prefix):
        node = self.search_prefix(prefix)  # Mencari node awalan
        words = []  # List kosong untuk menyimpan daftar kata yang ditemukan
        if node:  # Jika node awalan ditemukan
            # Panggil fungsi pencarian DFS (Depth First Search)
            self._dfs(node, prefix, words)
        return words  # Kembalikan daftar kata

    def _dfs(self, node, current_word, words):  # Fungsi rekursif DFS untuk menelusuri Trie
        if node.is_end_of_word:  # Jika node ini adalah akhir kata
            words.append(current_word)  # Tambahkan kata ke dalam list words
        for char, child_node in node.children.items():  # Iterasi semua anak dari node saat ini
            # Panggil DFS lagi dengan menambahkan huruf
            self._dfs(child_node, current_word + char, words)

# ==========================================
# 2. STRUKTUR DATA: DOUBLY LINKED LIST (Riwayat)
# ==========================================


class NodeDLL:  # Kelas untuk simpul (node) pada Doubly Linked List
    def __init__(self, data):  # Konstruktor node DLL
        self.data = data  # Menyimpan data (berupa kata yang dicari)
        self.prev = None  # Pointer untuk menunjuk ke node sebelumnya
        self.next = None  # Pointer untuk menunjuk ke node selanjutnya


class DoublyLinkedList:  # Kelas untuk Doubly Linked List itu sendiri
    def __init__(self):  # Konstruktor DLL
        self.head = None  # Pointer ke simpul pertama
        self.tail = None  # Pointer ke simpul terakhir
        # Pointer untuk menandai posisi saat ini (untuk Back/Forward)
        self.current = None

    def add(self, data):  # Fungsi menambahkan riwayat baru
        new_node = NodeDLL(data)  # Membuat node baru
        if self.head is None:  # Jika list masih kosong
            self.head = new_node  # Node baru menjadi kepala (head)
            self.tail = new_node  # Node baru menjadi ekor (tail)
            self.current = new_node  # Posisi saat ini berada di node baru
        else:  # Jika list tidak kosong
            new_node.prev = self.current  # Node baru menunjuk ke node saat ini sebagai prev
            self.current.next = new_node  # Node saat ini menunjuk ke node baru sebagai next
            self.tail = new_node  # Ekor diperbarui menjadi node baru
            self.current = new_node  # Posisi saat ini pindah ke node baru

    def go_back(self):  # Fungsi untuk mundur satu langkah di riwayat (Back)
        if self.current and self.current.prev:  # Jika ada posisi saat ini dan ada posisi sebelumnya
            self.current = self.current.prev  # Pindah ke posisi sebelumnya
            return self.current.data  # Kembalikan kata di posisi tersebut
        return None  # Jika tidak bisa mundur, kembalikan None

    def go_forward(self):  # Fungsi untuk maju satu langkah di riwayat (Forward)
        if self.current and self.current.next:  # Jika ada posisi saat ini dan ada posisi selanjutnya
            self.current = self.current.next  # Pindah ke posisi selanjutnya
            return self.current.data  # Kembalikan kata di posisi tersebut
        return None  # Jika tidak bisa maju, kembalikan None

# ==========================================
# 3. ALGORITMA LEVENSHTEIN (Fuzzy Search)
# ==========================================


# Fungsi untuk menghitung jarak perubahan antara dua kata
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):  # Jika s1 lebih pendek
        # Tukar posisi s1 dan s2 agar s1 selalu lebih panjang
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:  # Jika s2 kosong
        # Jaraknya adalah panjang s1 (harus menambah sebanyak panjang s1)
        return len(s1)

    previous_row = range(len(s2) + 1)  # Inisialisasi baris pertama perhitungan
    for i, c1 in enumerate(s1):  # Iterasi setiap karakter di kata pertama
        current_row = [i + 1]  # Baris saat ini diawali dengan indeks i+1
        for j, c2 in enumerate(s2):  # Iterasi setiap karakter di kata kedua
            # Hitung biaya jika menambah (insertion)
            insertions = previous_row[j + 1] + 1
            # Hitung biaya jika menghapus (deletion)
            deletions = current_row[j] + 1
            # Hitung biaya jika mengganti (substitution)
            substitutions = previous_row[j] + (c1 != c2)
            # Pilih biaya terkecil
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row  # Pindah ke baris berikutnya
    # Kembalikan nilai di pojok kanan bawah (jarak total)
    return previous_row[-1]


def get_fuzzy_suggestions(word, candidates, max_suggestions=4):
    # Tentukan toleransi typo berdasarkan panjang kata
    if len(word) <= 4:
        max_distance = 1
    elif len(word) <= 7:
        max_distance = 2
    else:
        max_distance = 3

    matches = []
    for candidate in candidates:
        if abs(len(candidate) - len(word)) > max_distance:
            continue
        dist = levenshtein_distance(word, candidate)
        if dist <= max_distance:
            matches.append((candidate, dist))

    matches.sort(key=lambda item: (item[1], item[0]))
    if matches:
        return matches[:max_suggestions]

    # Fallback ke difflib jika custom Levenshtein tidak menemukan hasil
    close_matches = difflib.get_close_matches(
        word, list(candidates), n=max_suggestions, cutoff=0.6)
    fallback = [(candidate, levenshtein_distance(word, candidate))
                for candidate in close_matches]
    fallback.sort(key=lambda item: (item[1], item[0]))
    return fallback[:max_suggestions]

# ==========================================
# 4. KELAS APLIKASI GUI UTAMA
# ==========================================


class KamusApp:  # Kelas utama untuk aplikasi
    def __init__(self, root):  # Konstruktor dengan parameter root (jendela Tkinter)
        self.root = root  # Menyimpan referensi jendela utama
        # Memberi judul pada jendela aplikasi
        self.root.title("Kamus Multi Guna")
        # Mengatur ukuran jendela menjadi 600x550 pixel
        self.root.geometry("600x550")

        self.hash_table = {}  # Inisialisasi Hash Table menggunakan dictionary bawaan Python
        self.trie = Trie()  # Menginisialisasi objek Trie untuk autocomplete
        # Menginisialisasi objek Doubly Linked List untuk riwayat
        self.history = DoublyLinkedList()
        # Menginisialisasi Set untuk menyimpan kata favorit (agar tidak ganda)
        self.favorites = set()

        self.load_data()  # Memanggil fungsi untuk memuat data JSON ke struktur data
        self.create_widgets()  # Memanggil fungsi untuk membuat elemen-elemen GUI

    def load_data(self):  # Fungsi membaca dan memasukkan data kamus
        # Mendapatkan folder tempat script ini berada
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Menentukan path file kamus baru secara absolut
        path_kamus = os.path.join(script_dir, "jeson", "kamus.json")
        if os.path.exists(path_kamus):  # Mengecek apakah file tersebut ada
            with open(path_kamus, 'r', encoding='utf-8') as f:  # Membuka file untuk dibaca
                data = json.load(f)  # Membaca file JSON
                for item in data:  # Iterasi setiap entri di dalam list JSON
                    # Mengambil kata bahasa Indonesia
                    indonesia = item.get("indonesia", "")
                    # Mengambil kata bahasa Inggris
                    inggris = item.get("inggris", "")
                    # Mengambil kata bahasa Sunda
                    sunda = item.get("sunda", "")
                    # Menggabungkan array sinonim menjadi string
                    sinonim = ", ".join(item.get("sinonim", []))
                    # Menggabungkan array antonim menjadi string
                    antonim = ", ".join(item.get("antonim", []))

                    # Format teks terjemahan yang akan ditampilkan
                    arti_teks = f"\n- Indonesia: {indonesia}\n- Inggris: {inggris}\n- Sunda: {sunda}"
                    if sinonim:
                        arti_teks += f"\n- Sinonim: {sinonim}"
                    if antonim:
                        arti_teks += f"\n- Antonim: {antonim}"

                    # Fungsi internal untuk menambahkan kata ke struktur data
                    def tambah_kata(kata):
                        if kata:  # Jika kata tidak kosong
                            kata_lower = kata.lower()  # Ubah ke huruf kecil
                            # Simpan teks arti ke Hash Table (Dictionary)
                            self.hash_table[kata_lower] = arti_teks
                            # Masukkan kata ke Trie untuk Autocomplete
                            self.trie.insert(kata_lower)

                    # Menambahkan semua bahasa agar bisa dicari dari bahasa mana pun
                    tambah_kata(indonesia)
                    tambah_kata(inggris)
                    tambah_kata(sunda)

    def create_widgets(self):  # Fungsi untuk mengatur tampilan GUI
        # Membuat sebuah frame penampung untuk area pencarian
        search_frame = tk.Frame(self.root)
        # Menempatkan frame dengan padding (jarak) atas-bawah 10
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Masukkan Kata:").pack(
            side=tk.LEFT)  # Menambahkan label teks

        self.entry_var = tk.StringVar()  # Variabel penampung teks untuk entry pencarian
        # Memicu fungsi on_typing setiap kali ada teks diketik
        self.entry_var.trace_add("write", self.on_typing)

        # Membuat input teks (Entry)
        self.entry = tk.Entry(
            search_frame, textvariable=self.entry_var, width=35)
        # Menempatkan input di sebelah kiri dengan padding samping 5
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.search_word())

        tk.Button(search_frame, text="Cari", command=self.search_word).pack(
            side=tk.LEFT)  # Membuat tombol Cari

        # Membuat kotak daftar (Listbox) untuk Autocomplete
        self.autocomplete_list = tk.Listbox(self.root, height=5, width=50)
        self.autocomplete_list.pack()  # Menempatkan Listbox ke dalam jendela
        # Jika item diklik, jalankan fungsi
        self.autocomplete_list.bind(
            "<<ListboxSelect>>", self.on_autocomplete_select)

        nav_frame = tk.Frame(self.root)  # Membuat frame untuk tombol navigasi
        nav_frame.pack(pady=10)  # Menempatkan frame dengan padding

        tk.Button(nav_frame, text="< Back", command=self.go_back).pack(
            side=tk.LEFT, padx=5)  # Membuat tombol Back
        tk.Button(nav_frame, text="Forward >", command=self.go_forward).pack(
            side=tk.LEFT, padx=5)  # Membuat tombol Forward
        tk.Button(nav_frame, text="Tambah Favorit", command=self.add_favorite).pack(
            side=tk.LEFT, padx=5)  # Tombol Tambah Favorit

        menu_frame = tk.Frame(self.root)  # Membuat frame untuk menu tambahan
        menu_frame.pack(pady=5)  # Menempatkan frame dengan padding

        tk.Button(menu_frame, text="Daftar Favorit", command=self.show_favorites).pack(
            side=tk.LEFT, padx=5)  # Tombol Lihat Favorit
        tk.Button(menu_frame, text="Mode Kuis", command=self.quiz_mode).pack(
            side=tk.LEFT, padx=5)  # Tombol untuk Kuis

        # Membuat area Teks hasil (Text)
        self.result_text = tk.Text(
            self.root, height=12, width=65, state=tk.DISABLED)
        self.result_text.pack(pady=10)  # Menempatkan area Teks dengan padding

    def on_typing(self, *args):  # Fungsi ini dijalankan saat user mengetik huruf
        # Mengambil huruf/kata yang sedang diketik
        prefix = self.entry_var.get().lower()
        # Mengosongkan daftar saran (autocomplete) sebelumnya
        self.autocomplete_list.delete(0, tk.END)
        if prefix:  # Jika kotak pencarian tidak kosong
            # Cari di Trie semua kata yang memiliki awalan ini
            words = self.trie.get_words_with_prefix(prefix)
            for w in words[:6]:  # Ambil maksimal 6 kata pertama saja
                # Masukkan kata tersebut ke Listbox untuk ditampilkan
                self.autocomplete_list.insert(tk.END, w)

    # Fungsi ini jalan jika user mengklik salah satu saran Autocomplete
    def on_autocomplete_select(self, event):
        # Cek baris ke berapa yang dipilih oleh user
        selection = event.widget.curselection()
        if selection:  # Jika ada baris yang dipilih
            # Ambil teks dari baris tersebut
            word = event.widget.get(selection[0])
            # Isi teks tersebut ke kotak input pencarian (Entry)
            self.entry_var.set(word)
            self.search_word()  # Langsung lakukan proses pencarian

    # Fungsi pembantu untuk menampilkan pesan di kotak Hasil (Text)
    def display_result(self, text):
        # Buka kunci edit Text agar bisa disisipi teks
        self.result_text.config(state=tk.NORMAL)
        # Hapus isi yang sudah ada sebelumnya
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)  # Tulis/sisipkan teks yang baru
        # Kunci kembali edit Text agar teks tidak bisa diubah user
        self.result_text.config(state=tk.DISABLED)

    def search_word(self, word_to_search=None):  # Fungsi utama mencari arti kata
        # Mengambil kata, membersihkan spasi depan/belakang
        word = word_to_search or self.entry_var.get().lower().strip()
        if not word:  # Jika kosong, batalkan
            return  # Keluar fungsi

        # 1. Cari kata langsung di Hash Table (Pencarian O(1))
        if word in self.hash_table:
            arti = self.hash_table[word]  # Jika ada, ambil artinya
            # Tampilkan kata dan artinya
            self.display_result(f"Kata: {word}\nArti: {arti}")
            # Jika dipanggil dari tombol cari (bukan dari Back/Forward)
            if not word_to_search:
                # Masukkan kata tersebut ke Doubly Linked List sebagai Riwayat
                self.history.add(word)
        else:
            # Info bahwa akan mencari saran
            self.display_result(
                f"Kata '{word}' tidak ditemukan.\nMencari saran...")
            self.root.update()  # Memaksa update tampilan GUI

            # 2. Fitur Typo / Fuzzy Search dengan Algoritma Levenshtein
            suggestions = get_fuzzy_suggestions(
                word, self.hash_table.keys(), max_suggestions=4)
            if suggestions:
                suggestion_lines = "\n".join(
                    f"- {candidate} (jarak {dist})" for candidate, dist in suggestions)
                best_word, best_dist = suggestions[0]
                arti = self.hash_table[best_word]
                self.display_result(
                    f"Kata '{word}' tidak ditemukan.\n\nMungkin maksud Anda:\n{suggestion_lines}\n\nArti '{best_word}': {arti}"
                )
            else:
                # Info jika gagal menebak typo
                self.display_result(
                    f"Kata '{word}' tidak ditemukan dan tidak ada saran kata yang cocok.")

    def go_back(self):  # Fungsi saat tombol < Back diklik
        # Mundur di Doubly Linked List dan ambil datanya
        prev_word = self.history.go_back()
        if prev_word:  # Jika berhasil (ada riwayat sebelumnya)
            # Ubah isi kotak pencarian jadi kata riwayat tersebut
            self.entry_var.set(prev_word)
            # Langsung jalankan pencarian untuk menampilkannya
            self.search_word(prev_word)

    def go_forward(self):  # Fungsi saat tombol Forward > diklik
        # Maju di Doubly Linked List dan ambil datanya
        next_word = self.history.go_forward()
        if next_word:  # Jika berhasil
            self.entry_var.set(next_word)  # Ubah isi kotak pencarian
            self.search_word(next_word)  # Langsung jalankan pencarian

    def add_favorite(self):  # Fungsi menyimpan daftar Favorit
        word = self.entry_var.get().lower().strip()  # Mengambil kata dari kotak input
        if word in self.hash_table:  # Memastikan bahwa kata tersebut valid dan ada artinya
            # Masukkan kata tersebut ke objek set `favorites`
            self.favorites.add(word)
            # Memunculkan pop-up pemberitahuan
            messagebox.showinfo(
                "Berhasil", f"'{word}' berhasil ditambahkan ke Favorit.")
        else:
            # Pop-up jika kata tidak valid
            messagebox.showwarning(
                "Gagal", "Silakan cari kata yang valid terlebih dahulu.")

    def show_favorites(self):  # Fungsi untuk melihat daftar kata Favorit
        if not self.favorites:  # Mengecek jika himpunan favorites masih kosong
            # Pop-up jika kosong
            messagebox.showinfo(
                "Daftar Favorit", "Belum ada kata favorit yang disimpan.")
            return  # Keluar dari fungsi
        # Menggabungkan semua kata favorit dengan baris baru (Enter)
        fav_list = "\n".join(self.favorites)
        # Memunculkan pop-up berisi daftar favorit
        messagebox.showinfo("Daftar Favorit", fav_list)

    def quiz_mode(self):  # Fungsi sederhana untuk Mode Kuis
        if not self.hash_table:  # Jika hash table belum ada data (batal)
            return  # Keluar dari fungsi
        # Mengacak satu kata dari kumpulan kata di Hash Table
        word = random.choice(list(self.hash_table.keys()))
        # Mengambil arti sebenarnya dari kata acak tersebut
        arti = self.hash_table[word]
        # Meminta jawaban user menggunakan Pop Up input
        answer = simpledialog.askstring(
            "Kuis", f"Apa terjemahan dari kata: '{word}'?")
        if answer:  # Jika user mengisi jawaban dan menekan OK
            # Menampilkan perbandingan jawaban user dengan hasil asli
            messagebox.showinfo(
                "Hasil Kuis", f"Jawaban Anda: {answer}\n\nArti Sebenarnya: {arti}")


if __name__ == "__main__":  # Bagian utama saat script dijalankan (entry point)
    root = tk.Tk()  # Memulai jendela utama antarmuka tkinter
    # Memanggil (inisialisasi) kelas KamusApp dengan root sebagai parameter
    app = KamusApp(root)
    root.mainloop()  # Memutar infinite loop GUI agar aplikasi tidak langsung tertutup
