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
# Mengelola seluruh tampilan dan logika interaksi pengguna
# ============================================================


class KamusApp:  # Kelas utama yang menyatukan semua modul aplikasi
    def __init__(self, root):  # Konstruktor: dipanggil saat aplikasi pertama dijalankan
        self.root = root                     # Simpan referensi jendela utama Tkinter
        self.root.title("Kamus Multi Guna")  # Judul yang tampil di title bar jendela

        self.hash_table   = HashTable()               # Hash Table: penyimpanan utama data kamus O(1)
        self.trie         = Trie()           # Trie: struktur untuk autocomplete
        self.history      = DoublyLinkedList() # DLL: navigasi riwayat pencarian
        self.favorites    = set()            # Set: daftar kata favorit (tidak duplikat)
        self.quiz_history = []               # List: menyimpan hasil sesi kuis

        self.load_data()        # Muat data kamus dari file JSON ke struktur data
        self.create_widgets()   # Bangun tampilan antarmuka grafis

    # ─────────────────────────────────────────────
    # MODUL 4B: PEMUATAN DATA KAMUS DARI JSON
    # Membaca file kamus.json dan mengisi Hash Table & Trie
    # ─────────────────────────────────────────────
    def load_data(self):  # Fungsi memuat dan memparsing data kamus dari file JSON
        script_dir  = os.path.dirname(os.path.abspath(__file__)) # Dapatkan folder lokasi script
        path_kamus  = os.path.join(script_dir, "dataset", "kamus.json") # Rangkai path file kamus
        self.kamus_data = []   # Inisialisasi list data mentah untuk keperluan mode kuis

        if os.path.exists(path_kamus):  # Cek apakah file kamus.json ada
            with open(path_kamus, 'r', encoding='utf-8') as f: # Buka file dengan encoding UTF-8
                data = json.load(f)          # Parse JSON menjadi list Python
                self.kamus_data = data       # Simpan data mentah untuk kuis
                for item in data:            # Iterasi setiap entri kata
                    indonesia = item.get("indonesia", "") # Ambil kata dalam bahasa Indonesia
                    inggris   = item.get("inggris",   "") # Ambil kata dalam bahasa Inggris
                    sunda     = item.get("sunda",     "") # Ambil kata dalam bahasa Sunda
                    sinonim   = ", ".join(item.get("sinonim", [])) # Gabung daftar sinonim
                    antonim   = ", ".join(item.get("antonim", [])) # Gabung daftar antonim

                    arti_teks = f"\n- Indonesia: {indonesia}\n- Inggris: {inggris}\n- Sunda: {sunda}"
                    if sinonim: arti_teks += f"\n- Sinonim: {sinonim}"
                    if antonim: arti_teks += f"\n- Antonim: {antonim}"

                    def tambah_kata(kata):
                        if kata:
                            k = kata.lower()
                            self.hash_table.set(k, arti_teks)
                            self.trie.insert(k)

                    tambah_kata(indonesia)
                    tambah_kata(inggris)
                    tambah_kata(sunda)

    # ─────────────────────────────────────────────
    # MODUL 4A: PEMBUATAN WIDGET GUI UTAMA
    # Membangun semua elemen tampilan jendela utama
    # ─────────────────────────────────────────────
    def create_widgets(self):
        # == Palet warna tema "Kalem" (muted steel-blue) ==
        C_BG     = "#f0f2f5"   # Abu-abu terang untuk latar belakang utama
        C_PANEL  = "#ffffff"   # Putih bersih untuk panel/kartu
        C_ACCENT = "#2563eb"   # Biru korporat sebagai warna aksen utama
        C_HEADER = "#1e3a5f"   # Biru tua gelap untuk header
        C_TEXT   = "#1e293b"   # Teks utama hampir hitam
        C_MUTED  = "#64748b"   # Teks sekunder abu-abu medium
        C_BORDER = "#cbd5e1"   # Garis batas abu-abu muda
        C_BTN    = "#334155"   # Tombol standar abu gelap
        C_INPUT  = "#ffffff"   # Latar kotak input putih
        C_RESULT = "#f8fafc"   # Latar area hasil sangat terang

        # == Ukuran & konfigurasi jendela utama ==
        self.root.configure(bg=C_BG)          # Terapkan warna latar belakang utama
        self.root.geometry("760x620")          # Ukuran jendela: lebar x tinggi (pixel)
        self.root.resizable(False, False)      # Larang pengubahan ukuran jendela

        # == BAGIAN HEADER: Judul aplikasi ==
        header = tk.Frame(self.root, bg=C_HEADER, pady=14) # Frame header biru tua
        header.pack(fill=tk.X)                # Bentangkan penuh secara horizontal
        tk.Label(                             # Label judul utama
            header, text="Kamus Multi Guna",
            font=("Segoe UI", 15, "bold"), bg=C_HEADER, fg="white"
        ).pack()
        tk.Label(                             # Label sub-judul bahasa
            header, text="Indonesia  ·  Inggris  ·  Sunda",
            font=("Segoe UI", 9), bg=C_HEADER, fg="#93c5fd"
        ).pack()

        # == BAGIAN PENCARIAN: Kotak input + tombol cari ==
        sf = tk.Frame(self.root, bg=C_PANEL, padx=18, pady=12, # Frame area pencarian
                      relief=tk.FLAT, bd=0)
        sf.pack(fill=tk.X, padx=14, pady=(12, 0))              # Tempatkan dengan margin

        tk.Label(sf, text="Cari Kata:", font=("Segoe UI", 10, "bold"), # Label "Cari Kata:"
                 bg=C_PANEL, fg=C_TEXT).grid(row=0, column=0, sticky="w", padx=(0,10))

        self.entry_var = tk.StringVar()                         # Variabel penampung teks input
        self.entry_var.trace_add("write", self.on_typing)       # Pantau perubahan ketikan

        self.entry = tk.Entry(                                  # Kotak input pencarian
            sf, textvariable=self.entry_var, width=48,
            font=("Segoe UI", 10), bg=C_INPUT, fg=C_TEXT,
            relief=tk.SOLID, bd=1
        )
        self.entry.grid(row=0, column=1, padx=(0, 8), sticky="we") # Tempatkan di kolom 1
        self.entry.bind("<Return>", lambda e: self.search_word())   # Enter = jalankan pencarian

        tk.Button(                                              # Tombol Cari berwarna biru
            sf, text="Cari", command=self.search_word,
            font=("Segoe UI", 10, "bold"), bg=C_ACCENT,
            fg="white", relief=tk.FLAT, padx=14, cursor="hand2"
        ).grid(row=0, column=2)

        # == BAGIAN AUTOCOMPLETE: Saran kata saat mengetik ==
        tk.Label(sf, text="Saran:", font=("Segoe UI", 8),      # Label kecil "Saran:"
                 bg=C_PANEL, fg=C_MUTED).grid(row=1, column=0, sticky="nw", pady=(6,0))

        self.autocomplete_list = tk.Listbox(                    # Listbox saran autocomplete
            sf, height=4, font=("Segoe UI", 10),
            bg=C_INPUT, fg=C_TEXT, selectbackground=C_ACCENT,
            selectforeground="white", relief=tk.SOLID, bd=1, activestyle="none"
        )
        self.autocomplete_list.grid(row=1, column=1, sticky="we", pady=(6,0)) # Tempatkan di bawah input
        self.autocomplete_list.bind("<<ListboxSelect>>", self.on_autocomplete_select) # Klik = pilih saran

        sf.grid_columnconfigure(1, weight=1)  # Kolom input bisa melebar

        # == BAGIAN TOOLBAR: Tombol navigasi dan menu ==
        toolbar = tk.Frame(self.root, bg=C_BG, pady=8)         # Frame toolbar tengah
        toolbar.pack(fill=tk.X, padx=14)

        def mkbtn(parent, text, cmd, bg=C_BTN):                # Helper pembuat tombol seragam
            return tk.Button(parent, text=text, command=cmd,
                             font=("Segoe UI", 9, "bold"), bg=bg,
                             fg="white", relief=tk.FLAT, padx=9, pady=4, cursor="hand2")

        # -- Navigasi kiri: Back & Forward --
        left = tk.Frame(toolbar, bg=C_BG)                      # Frame sisi kiri toolbar
        left.pack(side=tk.LEFT)
        mkbtn(left, "< Back",    self.go_back).pack(side=tk.LEFT, padx=(0,4))   # Tombol kembali riwayat
        mkbtn(left, "Forward >", self.go_forward).pack(side=tk.LEFT, padx=4)    # Tombol maju riwayat

        # -- Menu kanan: Favorit, Riwayat, Kuis --
        right = tk.Frame(toolbar, bg=C_BG)                     # Frame sisi kanan toolbar
        right.pack(side=tk.RIGHT)
        mkbtn(right, "Favorit",  self.add_favorite,  "#0f766e").pack(side=tk.LEFT, padx=4) # Tombol tambah favorit (hijau teal)
        mkbtn(right, "Daftar",   self.show_favorites, "#0369a1").pack(side=tk.LEFT, padx=4) # Tombol lihat daftar favorit (biru)
        mkbtn(right, "Riwayat",  self.show_history,   "#4338ca").pack(side=tk.LEFT, padx=4) # Tombol riwayat pencarian (indigo)
        mkbtn(right, "Kuis",     self.quiz_mode,      "#b45309").pack(side=tk.LEFT, padx=(4,0)) # Tombol mode kuis (cokelat)

        # == BAGIAN HASIL: Kotak tampilan hasil pencarian ==
        rf = tk.Frame(self.root, bg=C_PANEL, padx=14, pady=10) # Frame area hasil
        rf.pack(fill=tk.BOTH, expand=True, padx=14, pady=(6, 14))

        tk.Label(rf, text="Hasil Pencarian:", font=("Segoe UI", 10, "bold"), # Label judul area hasil
                 bg=C_PANEL, fg=C_TEXT).pack(anchor="w", pady=(0, 6))

        self.result_text = tk.Text(                             # Kotak teks hasil (read-only)
            rf, font=("Consolas", 10), bg=C_RESULT, fg=C_TEXT,
            state=tk.DISABLED, wrap=tk.WORD, padx=10, pady=10,
            relief=tk.SOLID, bd=1
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)       # Isi seluruh area yang tersedia

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

    def display_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)

    def search_word(self, word_to_search=None):
        word = word_to_search or self.entry_var.get().lower().strip()
        if not word:
            return

        if self.hash_table.contains(word):
            arti = self.hash_table.get(word)
            self.display_result(f"Kata: {word}\nArti: {arti}")
            if not word_to_search:
                self.history.add(word)
        else:
            self.display_result(f"Kata '{word}' tidak ditemukan.\nMencari saran...")
            self.root.update()

            suggestions = get_fuzzy_suggestions(word, self.hash_table.keys(), max_suggestions=4)
            if suggestions:
                suggestion_lines = "\n".join(
                    f"- {candidate} (jarak {dist})" for candidate, dist in suggestions)
                best_word, best_dist = suggestions[0]
                arti = self.hash_table.get(best_word)
                self.display_result(
                    f"Kata '{word}' tidak ditemukan.\n\nMungkin maksud Anda:\n{suggestion_lines}\n\nArti '{best_word}': {arti}"
                )
            else:
                self.display_result(
                    f"Kata '{word}' tidak ditemukan dan tidak ada saran kata yang cocok.")

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
                messagebox.showinfo("Info", f"'{word}' sudah ada di Daftar Favorit.")
            else:
                self.favorites.add(word)
                messagebox.showinfo("Berhasil", f"'{word}' ditambahkan ke Daftar Favorit!")
        else:
            messagebox.showwarning("Gagal", "Cari kata yang valid terlebih dahulu.")

    def show_favorites(self):
        win = tk.Toplevel(self.root)
        win.title("Daftar Favorit")
        win.geometry("500x380")
        win.resizable(False, False)

        tk.Label(win, text="Daftar Kata Favorit", font=("Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

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
                messagebox.showwarning("Peringatan", "Pilih kata yang ingin dihapus.", parent=win)
                return
            kata = str(tree.item(sel[0])["values"][1])
            self.favorites.discard(kata)
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

        tk.Label(win, text="Riwayat Pencarian", font=("Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

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
        if not hasattr(self, 'kamus_data') or not self.kamus_data:
            messagebox.showwarning("Data Kosong", "Data kamus tidak ditemukan atau kosong.")
            return

        sel = tk.Toplevel(self.root)
        sel.title("Pilih Mode Kuis")
        sel.geometry("380x300")
        sel.resizable(False, False)
        sel.grab_set()

        tk.Label(sel, text="Pilih Mode Kuis", font=("Segoe UI", 13, "bold"), pady=10).pack(fill=tk.X)
        tk.Label(sel, text="Pilih arah terjemahan untuk soal kuis:", font=("Segoe UI", 10)).pack(pady=(12, 6))

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
            messagebox.showwarning("Kuis Kosong", "Tidak cukup kosa kata untuk mode ini.")
            return

        MAX_SOAL = 10
        LABEL = {"indonesia": "Indonesia", "inggris": "Inggris", "sunda": "Sunda"}

        win = tk.Toplevel(self.root)
        win.title(f"Kuis {LABEL[field_soal]} → {LABEL[field_jawab]}")
        win.geometry("480x460")
        win.resizable(False, False)
        win.grab_set()

        state = {"benar": 0, "total": 0, "sudah_jawab": False, "kata": None}

        tk.Label(win, text=f"{LABEL[field_soal]} → {LABEL[field_jawab]}",
                 font=("Segoe UI", 13, "bold"), pady=10).pack(fill=tk.X)

        info_var = tk.StringVar(value=f"Soal 1 / {MAX_SOAL}  |  Skor: 0")
        tk.Label(win, textvariable=info_var, font=("Segoe UI", 10)).pack(pady=(8, 0))

        soal_var = tk.StringVar()
        tk.Label(win, textvariable=soal_var, font=("Segoe UI", 13, "bold"),
                 wraplength=430, pady=16, padx=16).pack(fill=tk.X, padx=14, pady=10)

        tk.Label(win, text=f"Jawab dalam bahasa {LABEL[field_jawab]}:", font=("Segoe UI", 9, "italic")).pack()

        jawaban_var = tk.StringVar()
        entry_jawab = tk.Entry(win, textvariable=jawaban_var, font=("Segoe UI", 12), justify="center")
        entry_jawab.pack(fill=tk.X, padx=14, pady=(4, 2))

        hint_var = tk.StringVar(value="Tekan Enter untuk menjawab")
        tk.Label(win, textvariable=hint_var, font=("Segoe UI", 8, "italic")).pack()

        feedback_var = tk.StringVar()
        lbl_feedback = tk.Label(win, textvariable=feedback_var, font=("Segoe UI", 10, "bold"))
        lbl_feedback.pack(pady=4)

        kunci_var = tk.StringVar()
        tk.Label(win, textvariable=kunci_var, font=("Consolas", 9),
                 wraplength=440, justify="left").pack(padx=14)

        def tampil_hasil():
            for w in win.winfo_children(): w.destroy()
            b, t = state["benar"], state["total"]
            persen = int(b / t * 100) if t > 0 else 0
            if persen >= 80:   pesan = "Luar Biasa!"
            elif persen >= 50: pesan = "Cukup Bagus!"
            else:              pesan = "Perlu Belajar Lagi!"

            import datetime
            mode_label = f"{LABEL[field_soal]} → {LABEL[field_jawab]}"
            self.quiz_history.append({
                "mode":   mode_label,
                "benar":  b,
                "total":  t,
                "persen": persen,
                "waktu":  datetime.datetime.now().strftime("%H:%M:%S")
            })

            tk.Label(win, text="Hasil Kuis", font=("Segoe UI", 14, "bold"), pady=10).pack(fill=tk.X)
            tk.Label(win, text=pesan, font=("Segoe UI", 18, "bold")).pack(pady=18)
            tk.Label(win, text=f"{b} / {t} Benar", font=("Segoe UI", 28, "bold")).pack()
            tk.Label(win, text=f"Persentase: {persen}%", font=("Segoe UI", 11)).pack(pady=(4, 20))
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
            soal_var.set(f"Apa kata {LABEL[field_jawab]} dari:\n\"{kata_soal}\"?")
            info_var.set(f"Soal {nomor} / {MAX_SOAL}  |  Skor: {state['benar']}")
            jawaban_var.set("")
            feedback_var.set("")
            kunci_var.set("")
            hint_var.set("Tekan Enter untuk menjawab")
            entry_jawab.config(state=tk.NORMAL)
            entry_jawab.focus()

        def periksa():
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
                if sinonim_str: kunci += f"\n→ Sinonim: {sinonim_str}"
                kunci_var.set(kunci)

            state["sudah_jawab"] = True
            entry_jawab.config(state=tk.DISABLED)
            info_var.set(f"Soal {state['total']} / {MAX_SOAL}  |  Skor: {state['benar']}")
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
        tk.Button(btn_f, text="Lewati", command=soal_baru, font=("Segoe UI", 10, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_f, text="Keluar", command=win.destroy, font=("Segoe UI", 10, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)

        soal_baru()

    def show_quiz_history(self):
        win = tk.Toplevel(self.root)
        win.title("Riwayat Kuis")
        win.geometry("560x360")
        win.resizable(False, False)

        tk.Label(win, text="Riwayat Kuis", font=("Segoe UI", 12, "bold"), pady=8).pack(fill=tk.X)

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
            tree.insert("", tk.END, values=("-", "-", "(Belum ada kuis)", "-", "-"))
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
            tree.insert("", tk.END, values=("-", "-", "(Belum ada kuis)", "-", "-"))

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