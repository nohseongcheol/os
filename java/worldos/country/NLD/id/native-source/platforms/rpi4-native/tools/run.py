#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/Jalankan_perintah.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('Jalankan_perintah', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('Jalankan_perintah')
    대응 = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'eksekusi_desktop', 'main': 'jalankan', 'host': 'host', 'status': 'Status_VALUE', 'NetworkBridge': 'jaringan_bridge', 'ROOT': 'Tugas_akar', 'bridge': 'bridge', 'loader': '적재기', 'base': 'wallpaper_VALUE', 'options': 'Opsi', 'binary': 'biner', 'args': 'argumen_ARRAY', 'command': 'perintah'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
