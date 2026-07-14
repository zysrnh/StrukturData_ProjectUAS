# ============================================================
# MODUL 5: STRUKTUR DATA HASH TABLE
# Digunakan untuk mencari arti kata dengan kompleksitas waktu O(1)
# ============================================================

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key):
        # Rumus mengubah teks kata menjadi angka (sebagai index laci penyimpanan)
        hash_val = 0
        for char in key:
            hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val

    def set(self, key, value):
        # Menyimpan kata (key) dan artinya (value) ke dalam Hash Table
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
            return

        current = self.table[index]
        while current:
            if current.key == key:
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = HashNode(key, value)
        self.size += 1

    def get(self, key, default=None):
        # Mengambil dan menampilkan arti dari suatu kata yang dicari
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return default

    def contains(self, key):
        # Mengecek apakah kata tersebut ada atau terdaftar di dalam kamus
        return self.get(key) is not None

    def keys(self):
        # Mengumpulkan dan mengambil semua daftar kata yang ada di dalam kamus
        keys_list = []
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                keys_list.append(current.key)
                current = current.next
        return keys_list
