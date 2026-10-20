from pengeluaran.cli import main


def jalankan(path, *argumen):
    return main(["--file", str(path), *argumen])


def test_alur_tambah_daftar_ringkasan_hapus(tmp_path, capsys):
    path = tmp_path / "data.json"
    kode = jalankan(path, "tambah", "--tanggal", "2026-10-15", "--kategori", "makan",
                    "--deskripsi", "Soto", "--jumlah", "14000")
    assert kode == 0
    jalankan(path, "daftar")
    assert "Soto" in capsys.readouterr().out
    jalankan(path, "ringkasan")
    assert "Total: Rp 14.000" in capsys.readouterr().out
    assert jalankan(path, "hapus", "1") == 0


def test_input_salah_mengembalikan_kode_1(tmp_path, capsys):
    path = tmp_path / "data.json"
    kode = jalankan(path, "tambah", "--tanggal", "salah", "--kategori", "makan",
                    "--deskripsi", "Soto", "--jumlah", "14000")
    assert kode == 1
    assert "Kesalahan" in capsys.readouterr().out
