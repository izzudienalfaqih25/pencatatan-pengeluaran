"""Pembuatan teks laporan yang ditampilkan ke pengguna."""

from typing import Dict, List

from pengeluaran.models import Pengeluaran


def format_rupiah(jumlah: int) -> str:
    """Contoh: 15000 -> 'Rp 15.000'."""
    return "Rp " + f"{jumlah:,}".replace(",", ".")


def tabel_pengeluaran(daftar: List[Pengeluaran]) -> str:
    """Buat tabel teks sederhana dari daftar pengeluaran."""
    if not daftar:
        return "Belum ada pengeluaran."
    baris = [f"{'ID':<4}{'Tanggal':<12}{'Kategori':<11}{'Jumlah':>12}  Deskripsi"]
    for p in daftar:
        baris.append(
            f"{p.id:<4}{p.tanggal:<12}{p.kategori:<11}{format_rupiah(p.jumlah):>12}  {p.deskripsi}"
        )
    return "\n".join(baris)


def teks_ringkasan(per_kategori: Dict[str, int]) -> str:
    """Buat ringkasan total per kategori beserta total keseluruhan."""
    if not per_kategori:
        return "Belum ada data untuk diringkas."
    baris = [f"- {kategori}: {format_rupiah(nilai)}" for kategori, nilai in sorted(per_kategori.items())]
    baris.append(f"Total: {format_rupiah(sum(per_kategori.values()))}")
    return "\n".join(baris)
