# Pencatat Pengeluaran

Aplikasi baris perintah (CLI) berbasis Python untuk mencatat pengeluaran harian, melihat daftar, dan meringkas total per kategori. Proyek ini dibuat untuk tugas mata kuliah DevSecOps (Pertemuan 5) dan dilengkapi pipeline CI/CD dengan pemindaian keamanan SAST.

## Fitur Utama

- Menambah pengeluaran (tanggal, kategori, deskripsi, jumlah) dengan validasi input.
- Melihat daftar pengeluaran, semua atau per kategori.
- Menghapus pengeluaran berdasarkan ID.
- Ringkasan total per kategori dan total keseluruhan.
- Data disimpan pada berkas JSON lokal.

Kategori yang tersedia: `makan`, `transport`, `belajar`, `hiburan`, `lainnya`.

## Teknologi

- Python 3.10 atau lebih baru (pipeline memakai Python 3.12)
- pytest untuk unit test
- GitHub Actions untuk CI/CD
- Semgrep sebagai SAST tool

## Struktur Folder

```
pencatat-pengeluaran/
├── .github/workflows/devsecops.yml   # pipeline GitHub Actions
├── .semgrep/rules.yml                # aturan Semgrep tambahan
├── pengeluaran/
│   ├── models.py                     # model data dan validasi
│   ├── storage.py                    # simpan/baca berkas JSON
│   ├── service.py                    # logika bisnis
│   ├── report.py                     # format tampilan teks
│   └── cli.py                        # perintah baris perintah
├── scripts/quality_gate.py           # pemeriksa Quality Gate
├── tests/                            # unit test
├── main.py                           # titik masuk aplikasi
├── requirements.txt
└── README.md
```

## Instalasi dan Menjalankan (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python main.py tambah --tanggal 2026-10-15 --kategori makan --deskripsi "Nasi goreng" --jumlah 15000
python main.py daftar
python main.py daftar --kategori makan
python main.py ringkasan
python main.py hapus 1
```

Data tersimpan di `data_pengeluaran.json` (dibuat otomatis, tidak ikut ke GitHub).

## Menjalankan Unit Test

```powershell
python -m pytest -v
```

## Pipeline DevSecOps

Workflow `.github/workflows/devsecops.yml` berjalan saat ada **push ke `main`** dan **pull request menuju `main`**, memakai runner `ubuntu-latest`, dengan dua job terpisah:

1. **`build`**: memasang dependensi, memeriksa sintaks (kompilasi), dan menjalankan unit test.
2. **`sast-scan`** (`needs: build`): memindai kode dengan Semgrep, menyimpan hasil JSON sebagai artifact, lalu menjalankan Quality Gate.

## SAST dan Quality Gate

**SAST** (*Static Application Security Testing*) memeriksa kode sumber tanpa menjalankan aplikasi. Alat yang dipakai adalah Semgrep dengan rule set `p/python` dan aturan lokal di `.semgrep/rules.yml`.

**Quality Gate** berupa skrip `scripts/quality_gate.py` yang membaca hasil pemindaian:

- Lulus jika temuan berseverity `ERROR` berjumlah 0.
- Gagal jika ada temuan `ERROR`, atau berkas hasil pemindaian tidak ada atau tidak terbaca.
- Temuan `WARNING` dan `INFO` hanya dilaporkan dan tidak menggagalkan pipeline.

Jika gagal, job `sast-scan` berstatus gagal (tanda silang merah) dan pull request tidak seharusnya digabung sebelum temuan diperbaiki.
