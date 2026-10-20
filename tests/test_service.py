import pytest

from pengeluaran.service import PencatatPengeluaran


def contoh():
    pencatat = PencatatPengeluaran()
    pencatat.tambah("2026-10-14", "makan", "Sarapan", 10000)
    pencatat.tambah("2026-10-14", "transport", "Ojek", 20000)
    pencatat.tambah("2026-10-15", "makan", "Makan siang", 15000)
    return pencatat


def test_tambah_memberi_id_berurutan():
    pencatat = contoh()
    assert [p.id for p in pencatat.daftar] == [1, 2, 3]


def test_total_seluruhnya_dan_per_kategori():
    pencatat = contoh()
    assert pencatat.total() == 45000
    assert pencatat.total("makan") == 25000


def test_ringkasan_per_kategori():
    assert contoh().ringkasan_per_kategori() == {"makan": 25000, "transport": 20000}


def test_hapus_dan_id_tidak_ada():
    pencatat = contoh()
    pencatat.hapus(2)
    assert pencatat.total() == 25000
    with pytest.raises(ValueError):
        pencatat.hapus(99)


def test_deskripsi_kosong_ditolak():
    with pytest.raises(ValueError):
        PencatatPengeluaran().tambah("2026-10-15", "makan", "   ", 1000)
