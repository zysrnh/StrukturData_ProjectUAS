# ============================================================
# MODUL 6: PENGUJIAN FITUR FAVORIT
# Digunakan untuk menguji fungsi simpan dan muat data kata favorit
# ============================================================

import json
import os
import tempfile
import unittest
import sys

# Menambahkan path agar bisa mengimpor KamusApp dari main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import KamusApp


class PengujianFavorit(unittest.TestCase):
    def test_simpan_dan_muat_favorit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "favorites.json")

            app = object.__new__(KamusApp)
            app.favorites = {"Halo", "World"}
            app.favorite_file_path = file_path
            app.save_favorites()

            with open(file_path, "r", encoding="utf-8") as f:
                saved_data = json.load(f)

            self.assertEqual(saved_data, ["Halo", "World"])

            reloaded = object.__new__(KamusApp)
            reloaded.favorites = set()
            reloaded.favorite_file_path = file_path
            reloaded.load_favorites()

            self.assertEqual(reloaded.favorites, {"halo", "world"})


if __name__ == "__main__":
    unittest.main()
