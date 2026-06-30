# ============================================================
# MODUL 2: STRUKTUR DATA DOUBLY LINKED LIST
# Digunakan untuk menyimpan dan menavigasi riwayat pencarian
# ============================================================

class NodeDLL:  # Kelas untuk satu simpul dalam Doubly Linked List
    def __init__(self, data):  # Konstruktor node dengan data kata
        self.data = data         # Data yang disimpan (nama kata yang dicari)
        self.prev = None         # Pointer ke simpul sebelumnya (untuk Back)
        self.next = None         # Pointer ke simpul berikutnya (untuk Forward)

class DoublyLinkedList:  # Kelas DLL sebagai manajer riwayat navigasi
    def __init__(self):  # Konstruktor DLL kosong
        self.head    = None      # Simpul pertama (kepala) DLL
        self.tail    = None      # Simpul terakhir (ekor) DLL
        self.current = None      # Simpul yang menunjukkan posisi navigasi saat ini

    def add(self, data):  # Fungsi menambah kata baru ke riwayat
        new_node = NodeDLL(data) # Buat simpul baru dengan data kata
        if self.head is None:    # Jika DLL masih kosong
            self.head = new_node     # Simpul baru menjadi kepala
            self.tail = new_node     # Simpul baru juga menjadi ekor
            self.current = new_node  # Posisi saat ini adalah simpul baru
        else:                    # Jika DLL sudah berisi data
            new_node.prev    = self.current      # Sambung ke simpul saat ini
            self.current.next = new_node         # Simpul saat ini menunjuk ke yang baru
            self.tail    = new_node              # Perbarui ekor ke simpul baru
            self.current = new_node              # Pindahkan posisi ke simpul baru

    def go_back(self):  # Fungsi mundur satu langkah (tombol Back)
        if self.current and self.current.prev:   # Pastikan ada simpul sebelumnya
            self.current = self.current.prev     # Pindah posisi ke simpul sebelumnya
            return self.current.data             # Kembalikan kata di posisi itu
        return None              # Tidak bisa mundur, kembalikan None

    def go_forward(self):  # Fungsi maju satu langkah (tombol Forward)
        if self.current and self.current.next:   # Pastikan ada simpul berikutnya
            self.current = self.current.next     # Pindah posisi ke simpul berikutnya
            return self.current.data             # Kembalikan kata di posisi itu
        return None              # Tidak bisa maju, kembalikan None
