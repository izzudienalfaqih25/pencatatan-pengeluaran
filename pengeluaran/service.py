"""Logika bisnis: menambah, menghapus, menyaring, dan menjumlahkan pengeluaran."""

from typing import Dict, List, Optional

from pengeluaran.models import (
    Pengeluaran,
    validasi_jumlah,
    validasi_kategori,
    validasi_tanggal,
)


class PencatatPengeluaran:
    """Mengelola kumpulan pengeluaran di memori."""

    def __init__(self, daftar: Optional[List[Pengeluaran]] = None):
        self.daftar: List[Pengeluaran] = list(daftar or [])

    def _id_berikutnya(self) -> int:
        """ID baru = ID terbesar saat ini + 1 (mulai dari 1)."""
        return max((p.id for p in self.daftar), default=0) + 1

    def tambah(self, tanggal: str, kategori: str, deskripsi: str, jumlah: int) -> Pengeluaran:
        """Tambah satu pengeluaran setelah semua input divalidasi."""
        deskripsi = deskripsi.strip()
        if not deskripsi:
            raise ValueError("Deskripsi tidak boleh kosong")
        baru = Pengeluaran(
            id=self._id_berikutnya(),
            tanggal=validasi_tanggal(tanggal),
            kategori=validasi_kategori(kategori),
            deskripsi=deskripsi,
            jumlah=validasi_jumlah(jumlah),
        )
        self.daftar.append(baru)
        return baru

    def hapus(self, id_pengeluaran: int) -> None:
        """Hapus pengeluaran berdasarkan ID. ID tidak ada -> ValueError."""
        for item in self.daftar:
            if item.id == id_pengeluaran:
                self.daftar.remove(item)
                return
        raise ValueError(f"Pengeluaran dengan ID {id_pengeluaran} tidak ditemukan")

    def daftar_pengeluaran(self, kategori: Optional[str] = None) -> List[Pengeluaran]:
        """Ambil semua pengeluaran, atau hanya satu kategori."""
        if kategori is None:
            return list(self.daftar)
        kategori = validasi_kategori(kategori)
        return [p for p in self.daftar if p.kategori == kategori]

    def total(self, kategori: Optional[str] = None) -> int:
        """Jumlahkan pengeluaran (seluruhnya atau per kategori)."""
        return sum(p.jumlah for p in self.daftar_pengeluaran(kategori))

    def ringkasan_per_kategori(self) -> Dict[str, int]:
        """Hitung total tiap kategori yang punya pengeluaran."""
        hasil: Dict[str, int] = {}
        for item in self.daftar:
            hasil[item.kategori] = hasil.get(item.kategori, 0) + item.jumlah
        return hasil
