"""Antarmuka baris perintah (command line) untuk aplikasi."""

import argparse
from typing import List, Optional

from pengeluaran import report, storage
from pengeluaran.service import PencatatPengeluaran

BERKAS_BAWAAN = "data_pengeluaran.json"


def buat_parser() -> argparse.ArgumentParser:
    """Definisikan semua perintah yang tersedia."""
    parser = argparse.ArgumentParser(description="Pencatat Pengeluaran Harian")
    parser.add_argument("--file", default=BERKAS_BAWAAN, help="lokasi berkas data JSON")
    sub = parser.add_subparsers(dest="perintah", required=True)

    tambah = sub.add_parser("tambah", help="tambah pengeluaran baru")
    tambah.add_argument("--tanggal", required=True, help="format YYYY-MM-DD")
    tambah.add_argument("--kategori", required=True)
    tambah.add_argument("--deskripsi", required=True)
    tambah.add_argument("--jumlah", required=True, type=int)

    lihat = sub.add_parser("daftar", help="tampilkan daftar pengeluaran")
    lihat.add_argument("--kategori", default=None)

    hapus = sub.add_parser("hapus", help="hapus pengeluaran berdasarkan ID")
    hapus.add_argument("id", type=int)

    sub.add_parser("ringkasan", help="total pengeluaran per kategori")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Jalankan perintah. Mengembalikan 0 jika sukses, 1 jika ada kesalahan input."""
    args = buat_parser().parse_args(argv)
    try:
        pencatat = PencatatPengeluaran(storage.muat(args.file))
        if args.perintah == "tambah":
            item = pencatat.tambah(args.tanggal, args.kategori, args.deskripsi, args.jumlah)
            storage.simpan(args.file, pencatat.daftar)
            print(f"Tersimpan dengan ID {item.id}: {report.format_rupiah(item.jumlah)}")
        elif args.perintah == "daftar":
            print(report.tabel_pengeluaran(pencatat.daftar_pengeluaran(args.kategori)))
        elif args.perintah == "hapus":
            pencatat.hapus(args.id)
            storage.simpan(args.file, pencatat.daftar)
            print(f"Pengeluaran ID {args.id} dihapus.")
        elif args.perintah == "ringkasan":
            print(report.teks_ringkasan(pencatat.ringkasan_per_kategori()))
    except ValueError as galat:
        print(f"Kesalahan: {galat}")
        return 1
    return 0
