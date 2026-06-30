# ============================================================
# MODUL 1: STRUKTUR DATA TRIE
# Digunakan untuk fitur autocomplete saat user mengetik kata
# ============================================================

class TrieNode:  # Kelas untuk satu simpul (node) dalam struktur pohon Trie
    def __init__(self):  # Konstruktor node
        self.children = {}           # Dict anak-node, kunci = huruf, nilai = TrieNode
        self.is_end_of_word = False   # True jika node ini adalah akhir dari sebuah kata

class Trie:  # Kelas pohon Trie sebagai wadah seluruh node
    def __init__(self):  # Konstruktor Trie
        self.root = TrieNode()       # Buat simpul akar (root) kosong sebagai titik awal

    def insert(self, word):  # Fungsi menyisipkan satu kata ke dalam Trie
        node = self.root             # Mulai penelusuran dari simpul akar
        for char in word:            # Iterasi tiap huruf dalam kata
            if char not in node.children:        # Jika huruf belum ada di anak-node
                node.children[char] = TrieNode() # Buat node baru untuk huruf tersebut
            node = node.children[char]           # Pindah ke node anak berikutnya
        node.is_end_of_word = True   # Tandai node terakhir sebagai akhir kata

    def search_prefix(self, prefix):  # Fungsi mencari node akhir dari awalan (prefix)
        node = self.root             # Mulai dari akar
        for char in prefix:          # Iterasi tiap huruf awalan
            if char not in node.children: # Jika huruf tidak ditemukan
                return None          # Awalan tidak ada, kembalikan None
            node = node.children[char]    # Pindah ke anak node
        return node                  # Kembalikan node terakhir awalan yang ditemukan

    def get_words_with_prefix(self, prefix):  # Ambil semua kata dengan awalan tertentu
        node = self.search_prefix(prefix)     # Cari node ujung awalan
        words = []                   # List untuk menampung hasil kata
        if node:                     # Jika awalan ditemukan
            self._dfs(node, prefix, words)    # Penelusuran DFS dari node tersebut
        return words                 # Kembalikan semua kata yang ditemukan

    def _dfs(self, node, current_word, words):  # Penelusuran DFS rekursif
        if node.is_end_of_word:      # Jika node ini adalah akhir kata
            words.append(current_word)          # Tambahkan kata ke hasil
        for char, child_node in node.children.items(): # Iterasi semua anak node
            self._dfs(child_node, current_word + char, words) # Rekursif dengan tambah huruf
