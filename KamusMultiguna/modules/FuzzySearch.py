import difflib

# ============================================================
# MODUL 3: ALGORITMA FUZZY SEARCH (Levenshtein Distance)
# Digunakan untuk koreksi typo dan saran kata yang mirip
# ============================================================

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)       # Baris awal matriks (indeks 0 s/d len(s2))
    for i, c1 in enumerate(s1):             # Iterasi setiap karakter di kata pertama
        current_row = [i + 1]               # Kolom pertama: biaya penghapusan bertahap
        for j, c2 in enumerate(s2):         # Iterasi setiap karakter di kata kedua
            insertions    = previous_row[j + 1] + 1    # Biaya penyisipan karakter
            deletions     = current_row[j] + 1         # Biaya penghapusan karakter
            substitutions = previous_row[j] + (c1 != c2) # Biaya penggantian karakter
            current_row.append(min(insertions, deletions, substitutions)) # Pilih minimum
        previous_row = current_row          # Geser baris untuk iterasi berikutnya
    return previous_row[-1]                 # Nilai kanan bawah = total jarak akhir

def get_fuzzy_suggestions(word, candidates, max_suggestions=5): # Cari saran kata mirip untuk koreksi typo
    # Tentukan toleransi kesalahan berdasarkan panjang kata
    if len(word) <= 2:        # Kata sangat pendek (1-2 huruf)
        max_distance = 1      # Toleransi: 1 perubahan saja
    elif len(word) <= 4:      # Kata pendek (3-4 huruf)
        max_distance = 2      # Toleransi: hingga 2 perubahan
    elif len(word) <= 7:      # Kata sedang (5-7 huruf)
        max_distance = 2      # Toleransi: 2 perubahan
    else:                     # Kata panjang (8+ huruf)
        max_distance = 3      # Toleransi: hingga 3 perubahan

    matches = []              # List penampung pasangan (kata, skor_jarak)
    for candidate in candidates:             # Iterasi semua kata di kamus
        if abs(len(candidate) - len(word)) > max_distance: # Lewati kata yang panjangnya jauh berbeda
            continue
        dist = levenshtein_distance(word, candidate) # Hitung jarak Levenshtein
        if dist <= max_distance and dist > 0:        # Jika dalam toleransi dan bukan kata sama
            prefix_bonus = 0                         # Inisialisasi bonus awalan
            if len(word) >= 2 and len(candidate) >= 2: # Jika kedua kata panjang nok
                if word[:2] == candidate[:2]:          # Jika 2 huruf awal sama
                    prefix_bonus = -0.5                # Beri bonus (kurangi skor = lebih relevan)
            matches.append((candidate, dist + prefix_bonus)) # Tambahkan ke daftar saran

    matches.sort(key=lambda item: (item[1], item[0])) # Urutkan: skor kecil dulu, lalu abjad
    if matches:               # Jika ada hasil dari Levenshtein
        return [(w, int(d)) for w, d in matches[:max_suggestions]] # Kembalikan maks N saran

    # Fallback: gunakan difflib jika Levenshtein tidak menemukan hasil
    close_matches = difflib.get_close_matches(
        word, list(candidates), n=max_suggestions, cutoff=0.45) # cutoff rendah = lebih permisif
    fallback = [(c, levenshtein_distance(word, c)) for c in close_matches] # Hitung ulang jarak
    fallback.sort(key=lambda item: (item[1], item[0]))  # Urutkan hasil fallback
    return fallback[:max_suggestions]       # Kembalikan hasil fallback
