import pytest

from pengeluaran.models import Pengeluaran, validasi_jumlah, validasi_kategori, validasi_tanggal


def test_bolak_balik_dict():
    asli = Pengeluaran(1, "2026-10-15", "makan", "Nasi goreng", 15000)
    assert Pengeluaran.dari_dict(asli.ke_dict()) == asli


def test_tanggal_valid_dan_tidak_valid():
    assert validasi_tanggal("2026-10-15") == "2026-10-15"
    with pytest.raises(ValueError):
        validasi_tanggal("15-10-2026")


def test_kategori_dinormalkan_dan_ditolak():
    assert validasi_kategori(" Makan ") == "makan"
    with pytest.raises(ValueError):
        validasi_kategori("judi")


@pytest.mark.parametrize("nilai", [0, -5])
def test_jumlah_harus_positif(nilai):
    with pytest.raises(ValueError):
        validasi_jumlah(nilai)
