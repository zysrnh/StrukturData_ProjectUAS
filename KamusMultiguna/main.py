# Mengimpor modul tkinter untuk membuat GUI (Antarmuka Pengguna)
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

from modules.Trie import Trie
from modules.DoublyLinkedList import DoublyLinkedList
from modules.FuzzySearch import get_fuzzy_suggestions
from modules.HashTable import HashTable

# ============================================================
# MODUL 4: KELAS APLIKASI GUI UTAMA (KamusApp)
# Mengelola antarmuka pengguna (GUI) dan interaksi utama aplikasi
# ============================================================

class KamusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kamus Multi Guna")

        # Inisialisasi struktur data (Pemanggilan dari modul)
        self.hash_table = HashTable()
        self.trie = Trie()
        self.history = DoublyLinkedList()
        self.favorites = set()
        self.quiz_history = []

        self.root.configure(bg="#f0f2f5")
        self.root.geometry("760x620")
        self.root.resizable(False, False)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.favorite_file_path = os.path.join(
            script_dir, "dataset", "favorites.json")
        self.load_favorites()
        self.load_data()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root, bg="#1e3a5f")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.welcome_frame, bg="#1e3a5f").pack(pady=70)

        tk.Label(self.welcome_frame, text="Kamus Multi Guna", font=(
            "Segoe UI", 32, "bold"), fg="white", bg="#1e3a5f").pack(pady=(0, 10))
        tk.Label(self.welcome_frame, text="Indonesia · Inggris · Sunda", font=(
            "Segoe UI", 14), fg="#93c5fd", bg="#1e3a5f").pack(pady=(0, 40))

        desc = "Aplikasi kamus pintar terintegrasi algoritma cerdas\n(Autocomplete, Typo Correction, dan Mode Kuis)."
        tk.Label(self.welcome_frame, text=desc, font=("Segoe UI", 12),
                 fg="#cbd5e1", bg="#1e3a5f", justify="center").pack(pady=(0, 50))

        btn_mulai = tk.Button(self.welcome_frame, text="Mulai Belajar", font=("Segoe UI", 12, "bold"), bg="#2563eb", fg="white",
                              padx=30, pady=10, relief=tk.FLAT, cursor="hand2", command=self.start_app)
        btn_mulai.pack()

    def start_app(self):
        self.welcome_frame.destroy()
        self.create_widgets()

    # ─────────────────────────────────────────────
    # MODUL 4B: PEMUATAN DATA KAMUS DARI JSON
    # Data Layer: Menyimpan & membaca data kamus dan favorit dari file JSON
    # Membaca file kamus.json dan mengisi Hash Table & Trie
    # ─────────────────────────────────────────────
    def load_data(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path_kamus = os.path.join(script_dir, "dataset", "kamus.json")
        self.kamus_data = []

        if os.path.exists(path_kamus):
            with open(path_kamus, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.kamus_data = data
                for item in data:
                    indonesia = item.get("indonesia", "")
                    inggris = item.get("inggris", "")
                    sunda = item.get("sunda", "")
                    sinonim = ", ".join(item.get("sinonim", []))
                    antonim = ", ".join(item.get("antonim", []))

                    arti_teks = f"\n- Indonesia: {indonesia}\n- Inggris: {inggris}\n- Sunda: {sunda}"
                    if sinonim:
                        arti_teks += f"\n- Sinonim: {sinonim}"
                    if antonim:
                        arti_teks += f"\n- Antonim: {antonim}"

                    def tambah_kata(kata):
                        if kata:
                            k = kata.lower()
                            self.hash_table.set(k, arti_teks)
                            self.trie.insert(k)

                    tambah_kata(indonesia)
                    tambah_kata(inggris)
                    tambah_kata(sunda)

    def load_favorites(self):
        if not hasattr(self, "favorite_file_path"):
            return

        if os.path.exists(self.favorite_file_path):
            try:
                with open(self.favorite_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.favorites = {str(item).strip().lower()
                                      for item in data if str(item).strip()}
                else:
                    self.favorites = set()
            # Error Handling: Mencegah error jika isi file JSON rusak atau gagal dibaca
            except (json.JSONDecodeError, OSError):
                self.favorites = set()
        else:
            self.favorites = set()

    def save_favorites(self):
        if not hasattr(self, "favorite_file_path"):
            return

        try:
            os.makedirs(os.path.dirname(
                self.favorite_file_path), exist_ok=True)
            with open(self.favorite_file_path, "w", encoding="utf-8") as f:
                json.dump(sorted(self.favorites), f,
                          ensure_ascii=False, indent=2)
                f.write("\n")
        # Error Handling: Mencegah error jika komputer menolak izin penyimpanan file
        except OSError:
            pass

    def on_close(self):
        self.save_favorites()
        self.root.destroy()

    # ─────────────────────────────────────────────
    # MODUL 4A: PEMBUATAN WIDGET GUI UTAMA
    # Membangun semua elemen tampilan jendela utama
    # ─────────────────────────────────────────────
    def create_widgets(self):
        # == Palet warna tema "Kalem" (muted steel-blue) ==
        C_BG = "#f0f2f5"   # Abu-abu terang untuk latar belakang utama
        C_PANEL = "#ffffff"   # Putih bersih untuk panel/kartu
        C_ACCENT = "#2563eb"   # Biru korporat sebagai warna aksen utama
        C_HEADER = "#1e3a5f"   # Biru tua gelap untuk header
        C_TEXT = "#1e293b"   # Teks utama hampir hitam
        C_MUTED = "#64748b"   # Teks sekunder abu-abu medium
        C_BORDER = "#cbd5e1"   # Garis batas abu-abu muda
        C_BTN = "#334155"   # Tombol standar abu gelap
        C_INPUT = "#ffffff"   # Latar kotak input putih
        C_RESULT = "#f8fafc"   # Latar area hasil sangat terang

        # == BAGIAN HEADER: Judul aplikasi ==
        # Frame header biru tua
        header = tk.Frame(self.root, bg=C_HEADER, pady=14)
        # Bentangkan penuh secara horizontal
        header.pack(fill=tk.X)
        tk.Label(                             # Label judul utama
            header, text="Kamus Multi Guna",
            font=("Segoe UI", 15, "bold"), bg=C_HEADER, fg="white"
        ).pack()
        tk.Label(                             # Label sub-judul bahasa
            header, text="Indonesia  ·  Inggris  ·  Sunda",
            font=("Segoe UI", 9), bg=C_HEADER, fg="#93c5fd"
        ).pack()

        # == BAGIAN PENCARIAN: Kotak input + tombol cari ==
        sf = tk.Frame(self.root, bg=C_PANEL, padx=18, pady=12,  # Frame area pencarian
                      relief=tk.FLAT, bd=0)
        # Tempatkan dengan margin
        sf.pack(fill=tk.X, padx=14, pady=(12, 0))

        tk.Label(sf, text="Cari Kata:", font=("Segoe UI", 10, "bold"),  # Label "Cari Kata:"
                 bg=C_PANEL, fg=C_TEXT).grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Variabel penampung teks input
        self.entry_var = tk.StringVar()
        # Pantau perubahan ketikan
        self.entry_var.trace_add("write", self.on_typing)

        self.entry = tk.Entry(                                  # Kotak input pencarian
            sf, textvariable=self.entry_var, width=48,
            font=("Segoe UI", 10), bg=C_INPUT, fg=C_TEXT,
            relief=tk.SOLID, bd=1
        )
        self.entry.grid(row=0, column=1, padx=(0, 8),
                        sticky="we")  # Tempatkan di kolom 1
        # Enter = jalankan pencarian
        self.entry.bind("<Return>", lambda e: self.search_word())

        tk.Button(                                              # Tombol Cari berwarna biru
            sf, text="Cari", command=self.search_word,
            font=("Segoe UI", 10, "bold"), bg=C_ACCENT,
            fg="white", relief=tk.FLAT, padx=14, cursor="hand2"
        ).grid(row=0, column=2)

        # == BAGIAN AUTOCOMPLETE: Saran kata saat mengetik ==
        tk.Label(sf, text="Saran:", font=("Segoe UI", 8),      # Label kecil "Saran:"
                 bg=C_PANEL, fg=C_MUTED).grid(row=1, column=0, sticky="nw", pady=(6, 0))

        self.autocomplete_list = tk.Listbox(                    # Listbox saran autocomplete
            sf, height=4, font=("Segoe UI", 10),
            bg=C_INPUT, fg=C_TEXT, selectbackground=C_ACCENT,
            selectforeground="white", relief=tk.SOLID, bd=1, activestyle="none"
        )
        # Tempatkan di bawah input
        self.autocomplete_list.grid(row=1, column=1, sticky="we", pady=(6, 0))
        self.autocomplete_list.bind(
            "<<ListboxSelect>>", self.on_autocomplete_select)  # Klik = pilih saran

        sf.grid_columnconfigure(1, weight=1)  # Kolom input bisa melebar

        # == BAGIAN TOOLBAR: Tombol navigasi dan menu ==
        # Frame toolbar tengah
        toolbar = tk.Frame(self.root, bg=C_BG, pady=8)
        toolbar.pack(fill=tk.X, padx=14)

        def mkbtn(parent, text, cmd, bg=C_BTN):                # Helper pembuat tombol seragam
            return tk.Button(parent, text=text, command=cmd,
                             font=("Segoe UI", 9, "bold"), bg=bg,
                             fg="white", relief=tk.FLAT, padx=9, pady=4, cursor="hand2")

        # -- Navigasi kiri: Back & Forward --
        # Frame sisi kiri toolbar
        left = tk.Frame(toolbar, bg=C_BG)
        left.pack(side=tk.LEFT)
        mkbtn(left, "< Back",    self.go_back).pack(
            side=tk.LEFT, padx=(0, 4))   # Tombol kembali riwayat
        mkbtn(left, "Forward >", self.go_forward).pack(
            side=tk.LEFT, padx=4)    # Tombol maju riwayat

        # -- Menu kanan: Favorit, Riwayat, Kuis --
        # Frame sisi kanan toolbar
        right = tk.Frame(toolbar, bg=C_BG)
        right.pack(side=tk.RIGHT)
        mkbtn(right, "Favorit",  self.add_favorite,  "#0f766e").pack(
            side=tk.LEFT, padx=4)  # Tombol tambah favorit (hijau teal)
        mkbtn(right, "Daftar",   self.show_favorites, "#0369a1").pack(
            side=tk.LEFT, padx=4)  # Tombol lihat daftar favorit (biru)
        mkbtn(right, "Riwayat",  self.show_history,   "#4338ca").pack(
            side=tk.LEFT, padx=4)  # Tombol riwayat pencarian (indigo)
        mkbtn(right, "Kuis",     self.quiz_mode,      "#b45309").pack(
            side=tk.LEFT, padx=(4, 0))  # Tombol mode kuis (cokelat)

        # == BAGIAN HASIL: Kotak tampilan hasil pencarian ==
        rf = tk.Frame(self.root, bg=C_PANEL, padx=14,
                      pady=10)  # Frame area hasil
        rf.pack(fill=tk.BOTH, expand=True, padx=14, pady=(6, 14))

        tk.Label(rf, text="Hasil Pencarian:", font=("Segoe UI", 10, "bold"),  # Label judul area hasil
                 bg=C_PANEL, fg=C_TEXT).pack(anchor="w", pady=(0, 6))

        self.result_text = tk.Text(                             # Kotak teks hasil (read-only)
            rf, font=("Segoe UI", 11), bg=C_RESULT, fg=C_TEXT,
            state=tk.DISABLED, wrap=tk.WORD, padx=20, pady=16,
            relief=tk.FLAT, bd=0
        )
        # Isi seluruh area yang tersedia
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Konfigurasi gaya teks (Rich Text)
        self.result_text.tag_configure("title", font=(
            "Segoe UI", 24, "bold"), foreground="#1e3a5f", spacing3=12)
        self.result_text.tag_configure("label", font=(
            "Segoe UI", 11, "bold"), foreground="#64748b", spacing1=6)
        self.result_text.tag_configure("value", font=(
            "Segoe UI", 12), foreground="#1e293b")
        self.result_text.tag_configure("info", font=(
            "Segoe UI", 12, "italic"), foreground="#b45309")

    def on_typing(self, *args):
        prefix = self.entry_var.get().lower()
        self.autocomplete_list.delete(0, tk.END)
        if prefix:
            words = self.trie.get_words_with_prefix(prefix)
            for w in words[:6]:
                self.autocomplete_list.insert(tk.END, w)

    def on_autocomplete_select(self, event):
        selection = event.widget.curselection()
        if selection:
            word = event.widget.get(selection[0])
            self.entry_var.set(word)
            self.search_word()

    def display_result(self, text, tag="info"):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text, tag)
        self.result_text.config(state=tk.DISABLED)

    def display_rich_result(self, word, arti_raw):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        # Cetak Judul Utama (Kata)
        self.result_text.insert(tk.END, f"{word.capitalize()}\n", "title")

        # Cetak rincian arti
        lines = arti_raw.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("- "):
                line = line[2:]  # Hilangkan strip

            if ":" in line:
                label, val = line.split(":", 1)
                self.result_text.insert(
                    tk.END, f"  {label.strip().upper()}   ", "label")
                self.result_text.insert(tk.END, f"{val.strip()}\n", "value")
            else:
                self.result_text.insert(tk.END, f"{line}\n", "value")

        self.result_text.config(state=tk.DISABLED)

    def search_word(self, word_to_search=None):
        word = word_to_search or self.entry_var.get().lower().strip()
        if not word:
            return

        if self.hash_table.contains(word):
            arti = self.hash_table.get(word)
            self.display_rich_result(word, arti)
            if not word_to_search:
                self.history.add(word)
        else:
            self.display_result(f"Mencari saran untuk '{word}'...", "info")
            self.root.update()

            # Memanggil algoritma Levenshtein untuk saran kata typo
            suggestions = get_fuzzy_suggestions(
                word, self.hash_table.keys(), max_suggestions=4)
            if suggestions:
                suggestion_lines = "\n".join(
                    f"- {candidate} (jarak {dist})" for candidate, dist in suggestions)
                best_word, best_dist = suggestions[0]
                arti = self.hash_table.get(best_word)
                self.display_result(
                    f"Kata '{word}' tidak ditemukan.\n\nMungkin maksud Anda:\n{suggestion_lines}\n\nArti '{best_word}': {arti}", "info"
                )
            else:
                self.display_result(
                    f"Kata '{word}' sama sekali tidak ditemukan.", "info")

    def go_back(self):
        prev_word = self.history.go_back()
        if prev_word:
            self.entry_var.set(prev_word)
            self.search_word(prev_word)

    def go_forward(self):
        next_word = self.history.go_forward()
        if next_word:
            self.entry_var.set(next_word)
            self.search_word(next_word)

    def add_favorite(self):
        word = self.entry_var.get().lower().strip()
        if self.hash_table.contains(word):
            if word in self.favorites:
                messagebox.showinfo(
                    "Info", f"'{word}' sudah ada di Daftar Favorit.")
            else:
                self.favorites.add(word)
                self.save_favorites()
                messagebox.showinfo(
                    "Berhasil", f"'{word}' ditambahkan ke Daftar Favorit!")
        else:
            # Error Handling: Validasi mencegah penambahan kata kosong atau tidak valid
            messagebox.showwarning(
                "Gagal", "Cari kata yang valid terlebih dahulu.")

    def show_favorites(self):
        win = tk.Toplevel(self.root)
        win.title("Daftar Favorit")
        win.geometry("500x380")
        win.resizable(False, False)

        tk.Label(win, text="Daftar Kata Favorit", font=(
            "Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

        columns = ("no", "kata", "arti")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
        tree.heading("no",   text="No")
        tree.heading("kata", text="Kata")
        tree.heading("arti", text="Terjemahan Singkat")
        tree.column("no",   width=40,  anchor="center")
        tree.column("kata", width=160, anchor="w")
        tree.column("arti", width=270, anchor="w")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if not self.favorites:
            tree.insert("", tk.END, values=("-", "(Belum ada favorit)", "-"))
        else:
            for i, kata in enumerate(sorted(self.favorites), 1):
                arti_raw = self.hash_table.get(kata, "")
                baris = arti_raw.strip().split("\n")
                singkat = baris[1].strip() if len(baris) > 1 else arti_raw[:40]
                tree.insert("", tk.END, values=(i, kata, singkat))

        def hapus():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning(
                    "Peringatan", "Pilih kata yang ingin dihapus.", parent=win)
                return
            kata = str(tree.item(sel[0])["values"][1])
            self.favorites.discard(kata)
            self.save_favorites()
            tree.delete(sel[0])

        btn_f = tk.Frame(win)
        btn_f.pack(pady=(0, 10))
        tk.Button(btn_f, text="Hapus Terpilih", command=hapus, font=("Segoe UI", 9, "bold"),
                  padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Tutup", command=win.destroy, font=("Segoe UI", 9, "bold"),
                  padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=5)

    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("Riwayat Pencarian")
        win.geometry("500x380")
        win.resizable(False, False)

        tk.Label(win, text="Riwayat Pencarian", font=(
            "Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

        columns = ("no", "kata", "arti")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
        tree.heading("no",   text="No")
        tree.heading("kata", text="Kata Dicari")
        tree.heading("arti", text="Terjemahan Singkat")
        tree.column("no",   width=40,  anchor="center")
        tree.column("kata", width=160, anchor="w")
        tree.column("arti", width=270, anchor="w")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        riwayat = []
        node = self.history.head
        while node:
            riwayat.append(node.data)
            node = node.next

        if not riwayat:
            tree.insert("", tk.END, values=("-", "(Belum ada riwayat)", "-"))
        else:
            for i, kata in enumerate(riwayat, 1):
                arti_raw = self.hash_table.get(kata, "-")
                baris = arti_raw.strip().split("\n")
                singkat = baris[1].strip() if len(baris) > 1 else arti_raw[:40]
                tree.insert("", tk.END, values=(i, kata, singkat))

            if self.history.current and self.history.current.data in riwayat:
                idx = riwayat.index(self.history.current.data)
                children = tree.get_children()
                if idx < len(children):
                    tree.selection_set(children[idx])
                    tree.see(children[idx])

        tk.Button(win, text="Tutup", command=win.destroy, font=("Segoe UI", 9, "bold"),
                  padx=10, pady=4, cursor="hand2").pack(pady=(0, 10))

    def quiz_mode(self):
        # Error Handling: Validasi mencegah error jika database kamus kosong
        if not hasattr(self, 'kamus_data') or not self.kamus_data:
            messagebox.showwarning(
                "Data Kosong", "Data kamus tidak ditemukan atau kosong.")
            return

        sel = tk.Toplevel(self.root)
        sel.title("Pilih Mode Kuis")
        sel.geometry("380x360")
        sel.resizable(False, False)
        sel.grab_set()

        tk.Label(sel, text="Pilih Mode Kuis", font=(
            "Segoe UI", 13, "bold"), pady=10).pack(fill=tk.X)
        tk.Label(sel, text="Pilih arah terjemahan untuk soal kuis:",
                 font=("Segoe UI", 10)).pack(pady=(12, 6))

        MODE_LIST = [
            ("Indonesia  →  Sunda",    "indonesia", "sunda"),
            ("Sunda      →  Indonesia", "sunda",     "indonesia"),
            ("Inggris   →  Indonesia", "inggris",   "indonesia"),
            ("Indonesia →  Inggris",   "indonesia", "inggris"),
        ]

        def mulai_kuis(field_soal, field_jawab):
            sel.destroy()
            self._jalankan_kuis(field_soal, field_jawab)

        for label, fs, fj in MODE_LIST:
            tk.Button(sel, text=label, font=("Segoe UI", 10, "bold"),
                      padx=10, pady=6, cursor="hand2",
                      command=lambda f1=fs, f2=fj: mulai_kuis(f1, f2)
                      ).pack(fill=tk.X, padx=24, pady=4)

        btn_bot = tk.Frame(sel)
        btn_bot.pack(pady=(8, 6))
        tk.Button(btn_bot, text="Riwayat Kuis", command=lambda: self.show_quiz_history(),
                  font=("Segoe UI", 9, "bold"), padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_bot, text="Batal", command=sel.destroy, font=("Segoe UI", 9),
                  padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=4)

    def _jalankan_kuis(self, field_soal, field_jawab):
        entri_valid = [
            item for item in self.kamus_data
            if item.get(field_soal, "").strip() and item.get(field_jawab, "").strip()
        ]
        if not entri_valid:
            # Error Handling: Validasi mencegah kuis error jika jumlah kosa kata kurang
            messagebox.showwarning(
                "Kuis Kosong", "Tidak cukup kosa kata untuk mode ini.")
            return

        MAX_SOAL = 10
        LABEL = {"indonesia": "Indonesia",
                 "inggris": "Inggris", "sunda": "Sunda"}

        win = tk.Toplevel(self.root)
        win.title(f"Kuis {LABEL[field_soal]} → {LABEL[field_jawab]}")
        win.geometry("480x460")
        win.resizable(False, False)
        win.grab_set()

        state = {"benar": 0, "total": 0, "sudah_jawab": False, "kata": None}

        tk.Label(win, text=f"{LABEL[field_soal]} → {LABEL[field_jawab]}",
                 font=("Segoe UI", 13, "bold"), pady=10).pack(fill=tk.X)

        info_var = tk.StringVar(value=f"Soal 1 / {MAX_SOAL}  |  Skor: 0")
        tk.Label(win, textvariable=info_var, font=(
            "Segoe UI", 10)).pack(pady=(8, 0))

        soal_var = tk.StringVar()
        tk.Label(win, textvariable=soal_var, font=("Segoe UI", 13, "bold"),
                 wraplength=430, pady=16, padx=16).pack(fill=tk.X, padx=14, pady=10)

        tk.Label(win, text=f"Jawab dalam bahasa {LABEL[field_jawab]}:", font=(
            "Segoe UI", 9, "italic")).pack()

        jawaban_var = tk.StringVar()
        entry_jawab = tk.Entry(win, textvariable=jawaban_var, font=(
            "Segoe UI", 12), justify="center")
        entry_jawab.pack(fill=tk.X, padx=14, pady=(4, 2))

        hint_var = tk.StringVar(value="Tekan Enter untuk menjawab")
        tk.Label(win, textvariable=hint_var, font=(
            "Segoe UI", 8, "italic")).pack()

        feedback_var = tk.StringVar()
        lbl_feedback = tk.Label(
            win, textvariable=feedback_var, font=("Segoe UI", 10, "bold"))
        lbl_feedback.pack(pady=4)

        kunci_var = tk.StringVar()
        tk.Label(win, textvariable=kunci_var, font=("Consolas", 9),
                 wraplength=440, justify="left").pack(padx=14)

        def tampil_hasil():
            for w in win.winfo_children():
                w.destroy()
            b, t = state["benar"], state["total"]
            persen = int(b / t * 100) if t > 0 else 0
            if persen >= 80:
                pesan = "Luar Biasa!"
            elif persen >= 50:
                pesan = "Cukup Bagus!"
            else:
                pesan = "Perlu Belajar Lagi!"

            import datetime
            mode_label = f"{LABEL[field_soal]} → {LABEL[field_jawab]}"
            self.quiz_history.append({
                "mode":   mode_label,
                "benar":  b,
                "total":  t,
                "persen": persen,
                "waktu":  datetime.datetime.now().strftime("%H:%M:%S")
            })

            tk.Label(win, text="Hasil Kuis", font=(
                "Segoe UI", 14, "bold"), pady=10).pack(fill=tk.X)
            tk.Label(win, text=pesan, font=(
                "Segoe UI", 18, "bold")).pack(pady=18)
            tk.Label(win, text=f"{b} / {t} Benar",
                     font=("Segoe UI", 28, "bold")).pack()
            tk.Label(win, text=f"Persentase: {persen}%", font=(
                "Segoe UI", 11)).pack(pady=(4, 20))
            tk.Button(win, text="Tutup", command=win.destroy, font=("Segoe UI", 10, "bold"),
                      padx=16, pady=6, cursor="hand2").pack()

        def soal_baru():
            if state["total"] >= MAX_SOAL:
                tampil_hasil()
                return
            state["sudah_jawab"] = False
            item = random.choice(entri_valid)
            state["kata"] = item
            nomor = state["total"] + 1
            kata_soal = item.get(field_soal, "")
            soal_var.set(
                f"Apa kata {LABEL[field_jawab]} dari:\n\"{kata_soal}\"?")
            info_var.set(
                f"Soal {nomor} / {MAX_SOAL}  |  Skor: {state['benar']}")
            jawaban_var.set("")
            feedback_var.set("")
            kunci_var.set("")
            hint_var.set("Tekan Enter untuk menjawab")
            entry_jawab.config(state=tk.NORMAL)
            entry_jawab.focus()

        def periksa():
            if state["sudah_jawab"]:
                return
            jawaban = jawaban_var.get().strip().lower()
            if not jawaban:
                return
            item = state["kata"]
            jawaban_benar = [item.get(field_jawab, "").lower()]
            for sin in item.get("sinonim", []):
                jawaban_benar.append(sin.strip().lower())

            state["total"] += 1
            if jawaban in jawaban_benar:
                state["benar"] += 1
                feedback_var.set("Benar! Hebat!")
                kunci_var.set("")
            else:
                feedback_var.set("Salah! Jawaban yang benar:")
                jawaban_utama = item.get(field_jawab, "")
                sinonim_str = ", ".join(item.get("sinonim", []))
                kunci = f"→ {LABEL[field_jawab]}: {jawaban_utama}"
                if sinonim_str:
                    kunci += f"\n→ Sinonim: {sinonim_str}"
                kunci_var.set(kunci)

            state["sudah_jawab"] = True
            entry_jawab.config(state=tk.DISABLED)
            info_var.set(
                f"Soal {state['total']} / {MAX_SOAL}  |  Skor: {state['benar']}")
            if state["total"] >= MAX_SOAL:
                hint_var.set("Tekan Enter untuk melihat hasil akhir")
            else:
                hint_var.set("Tekan Enter untuk soal berikutnya")

        def enter_handler(e):
            if state.get("sudah_jawab", False):
                soal_baru()
            else:
                periksa()

        entry_jawab.bind("<Return>", enter_handler)

        btn_f = tk.Frame(win)
        btn_f.pack(pady=8)
        tk.Button(btn_f, text="Jawab", command=periksa, font=("Segoe UI", 10, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_f, text="Selanjutnya", command=soal_baru, font=("Segoe UI", 10, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_f, text="Keluar", command=win.destroy, font=("Segoe UI", 10, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)

        soal_baru()

    def show_quiz_history(self):
        win = tk.Toplevel(self.root)
        win.title("Riwayat Kuis")
        win.geometry("560x360")
        win.resizable(False, False)

        tk.Label(win, text="Riwayat Kuis", font=(
            "Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

        cols = ("no", "waktu", "mode", "skor", "persen")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=9)
        tree.heading("no",     text="No")
        tree.heading("waktu",  text="Waktu")
        tree.heading("mode",   text="Mode")
        tree.heading("skor",   text="Skor")
        tree.heading("persen", text="Nilai")
        tree.column("no",     width=35,  anchor="center")
        tree.column("waktu",  width=75,  anchor="center")
        tree.column("mode",   width=210, anchor="w")
        tree.column("skor",   width=70,  anchor="center")
        tree.column("persen", width=80,  anchor="center")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if not self.quiz_history:
            tree.insert("", tk.END, values=(
                "-", "-", "(Belum ada kuis)", "-", "-"))
        else:
            for i, rec in enumerate(self.quiz_history, 1):
                p = rec["persen"]
                nilai = f"{p}%  {'(Luar Biasa)' if p>=80 else '(Cukup Bagus)' if p>=50 else '(Perlu Belajar)'}"
                tree.insert("", tk.END, values=(
                    i,
                    rec["waktu"],
                    rec["mode"],
                    f"{rec['benar']} / {rec['total']}",
                    nilai
                ))

        def hapus_semua():
            self.quiz_history.clear()
            for row in tree.get_children():
                tree.delete(row)
            tree.insert("", tk.END, values=(
                "-", "-", "(Belum ada kuis)", "-", "-"))

        btn_f = tk.Frame(win)
        btn_f.pack(pady=(0, 10))
        tk.Button(btn_f, text="Hapus Semua", command=hapus_semua, font=("Segoe UI", 9, "bold"),
                  padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Tutup", command=win.destroy, font=("Segoe UI", 9, "bold"),
                  padx=10, pady=4, cursor="hand2").pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = KamusApp(root)
    root.mainloop()
