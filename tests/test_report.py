from pengeluaran.models import Pengeluaran
from pengeluaran.report import format_rupiah, tabel_pengeluaran, teks_ringkasan


def test_format_rupiah():
    assert format_rupiah(15000) == "Rp 15.000"
    assert format_rupiah(1250000) == "Rp 1.250.000"


def test_tabel_kosong_dan_berisi():
    assert tabel_pengeluaran([]) == "Belum ada pengeluaran."
    teks = tabel_pengeluaran([Pengeluaran(1, "2026-10-15", "makan", "Bakso", 12000)])
    assert "Bakso" in teks and "Rp 12.000" in teks


def test_ringkasan_memuat_total():
    teks = teks_ringkasan({"makan": 10000, "transport": 5000})
    assert "Total: Rp 15.000" in teks
