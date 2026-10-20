"""Penyimpanan data pengeluaran ke berkas JSON."""

import json
import os
from typing import List

from pengeluaran.models import Pengeluaran


def muat(path: str) -> List[Pengeluaran]:
    """Baca daftar pengeluaran dari berkas. Berkas belum ada -> daftar kosong."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as berkas:
            isi = json.load(berkas)
    except json.JSONDecodeError:
        raise ValueError(f"Berkas data rusak atau bukan JSON yang valid: {path}")
    return [Pengeluaran.dari_dict(item) for item in isi]


def simpan(path: str, daftar: List[Pengeluaran]) -> None:
    """Tulis seluruh daftar pengeluaran ke berkas JSON."""
    with open(path, "w", encoding="utf-8") as berkas:
        json.dump([p.ke_dict() for p in daftar], berkas, indent=2, ensure_ascii=False)
