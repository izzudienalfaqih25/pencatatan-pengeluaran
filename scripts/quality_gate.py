"""Quality Gate: membaca hasil Semgrep (JSON) dan menentukan lulus atau gagal.

Kriteria kelulusan:
  - Temuan berseverity ERROR harus 0.
  - Temuan WARNING / INFO hanya dilaporkan dan tidak menggagalkan pipeline.
Berkas hasil yang tidak ada atau tidak terbaca juga dianggap GAGAL.
"""

import json
import sys

BATAS_ERROR = 0


def main(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as berkas:
            hasil = json.load(berkas)
    except (OSError, json.JSONDecodeError) as galat:
        print(f"GAGAL: hasil pemindaian tidak dapat dibaca ({galat})")
        return 1

    temuan = hasil.get("results", [])
    hitung = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for item in temuan:
        tingkat = item.get("extra", {}).get("severity", "INFO")
        hitung[tingkat] = hitung.get(tingkat, 0) + 1

    print("=== RINGKASAN QUALITY GATE ===")
    print(f"Total temuan : {len(temuan)}")
    for tingkat, jumlah in hitung.items():
        print(f"  {tingkat:<8}: {jumlah}")
    for item in temuan:
        print(f"- [{item['extra']['severity']}] {item['path']}:{item['start']['line']} {item['check_id']}")

    if hitung["ERROR"] > BATAS_ERROR:
        print(f"HASIL: GAGAL (temuan ERROR {hitung['ERROR']} > batas {BATAS_ERROR})")
        return 1
    print("HASIL: LULUS")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cara pakai: python scripts/quality_gate.py semgrep-results.json")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
