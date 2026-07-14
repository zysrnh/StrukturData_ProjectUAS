# ============================================================
# MODUL 1: STRUKTUR DATA TRIE
# Digunakan untuk fitur autocomplete saat user mengetik kata
# ============================================================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # Memasukkan kata baru ke dalam struktur Trie huruf demi huruf
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        # Mencari apakah ada cabang huruf yang cocok dengan awalan (prefix) yang diketik
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_words_with_prefix(self, prefix):
        # Mengambil semua daftar kata lengkap yang berawalan sesuai input (untuk autocomplete)
        node = self.search_prefix(prefix)
        words = []
        if node:
            self._dfs(node, prefix, words)
        return words

    def _dfs(self, node, current_word, words):
        # Algoritma penelusuran (DFS) untuk merangkai huruf menjadi kata yang utuh
        if node.is_end_of_word:
            words.append(current_word)
        for char, child_node in node.children.items():
            self._dfs(child_node, current_word + char, words)
