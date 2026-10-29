#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/Buat_foto.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('Buat_foto', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('Buat_foto')
    대응 = {'total': 'total_kapasitas', 'start': 'jalankan', 'firmware': '기초제어프로그램', 'files': 'file_Daftar', 'archive_base': 'Arsip_BASE', 'partition': 'partisi_file', 'archive': 'Arsip', 'main': 'jalankan', 'block': 'blok_data', 'ROOT': 'Tugas_akar', 'boot': '부팅경로', 'stage': 'tahap_VALUE', 'out': 'KR_data', 'expected': '예상결과', 'f': 'file_entri', 'src': '원본주소', 'path': 'jalur', 'p': 'data_posisi', 'extracted': '추출자료', 'member': 'anggota', 'mbr': 'rekaman_awal_utama', 'image': 'foto', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lisensi', 'source': '원본자료', 'name': 'Nama_2', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'tujuan_VALUE_posisi', 'work': '작업경로'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
