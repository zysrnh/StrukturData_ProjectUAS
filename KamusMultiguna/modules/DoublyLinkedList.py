# ============================================================
# MODUL 2: STRUKTUR DATA DOUBLY LINKED LIST
# Digunakan untuk menyimpan dan menavigasi riwayat pencarian
# ============================================================

class NodeDLL:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add(self, data):
        # Menyimpan kata baru yang baru saja dicari ke dalam daftar riwayat
        new_node = NodeDLL(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.current
            self.current.next = new_node
            self.tail = new_node
            self.current = new_node

    def go_back(self):
        # Mundur satu langkah untuk melihat kata yang dicari sebelumnya
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.data
        return None

    def go_forward(self):
        # Maju satu langkah ke kata yang dicari setelahnya
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.data
        return None
