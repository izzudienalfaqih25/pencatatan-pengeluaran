import pytest

from pengeluaran import storage
from pengeluaran.models import Pengeluaran


def test_berkas_belum_ada_memberi_daftar_kosong(tmp_path):
    assert storage.muat(str(tmp_path / "tidak_ada.json")) == []


def test_simpan_lalu_muat(tmp_path):
    path = str(tmp_path / "data.json")
    data = [Pengeluaran(1, "2026-10-15", "belajar", "Buku", 50000)]
    storage.simpan(path, data)
    assert storage.muat(path) == data


def test_berkas_rusak_memicu_error(tmp_path):
    path = tmp_path / "rusak.json"
    path.write_text("{bukan json", encoding="utf-8")
    with pytest.raises(ValueError):
        storage.muat(str(path))
