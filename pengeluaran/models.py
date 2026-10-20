"""Model data: satu catatan pengeluaran dan aturan validasinya."""

from dataclasses import asdict, dataclass
from datetime import date

# Kategori yang boleh dipakai pada aplikasi
KATEGORI_VALID = ("makan", "transport", "belajar", "hiburan", "lainnya")


@dataclass
class Pengeluaran:
    """Satu baris catatan pengeluaran."""

    id: int
    tanggal: str  # format YYYY-MM-DD
    kategori: str
    deskripsi: str
    jumlah: int  # dalam rupiah

    def ke_dict(self) -> dict:
        """Ubah objek menjadi dictionary agar bisa disimpan ke JSON."""
        return asdict(self)

    @staticmethod
    def dari_dict(data: dict) -> "Pengeluaran":
        """Buat objek dari dictionary hasil pembacaan JSON."""
        return Pengeluaran(
            id=int(data["id"]),
            tanggal=str(data["tanggal"]),
            kategori=str(data["kategori"]),
            deskripsi=str(data["deskripsi"]),
            jumlah=int(data["jumlah"]),
        )


def validasi_tanggal(teks: str) -> str:
    """Pastikan tanggal berformat YYYY-MM-DD dan benar-benar ada."""
    try:
        return date.fromisoformat(teks).isoformat()
    except ValueError:
        raise ValueError("Tanggal harus berformat YYYY-MM-DD, contoh 2026-10-15")


def validasi_kategori(kategori: str) -> str:
    """Pastikan kategori termasuk dalam daftar yang diizinkan."""
    kategori = kategori.strip().lower()
    if kategori not in KATEGORI_VALID:
        pilihan = ", ".join(KATEGORI_VALID)
        raise ValueError(f"Kategori tidak dikenal. Pilihan: {pilihan}")
    return kategori


def validasi_jumlah(jumlah: int) -> int:
    """Pastikan jumlah uang berupa bilangan bulat positif."""
    if not isinstance(jumlah, int) or jumlah <= 0:
        raise ValueError("Jumlah harus berupa bilangan bulat lebih dari 0")
    return jumlah
