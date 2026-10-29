#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/crea_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('crea_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('crea_IMAGE')
    mapare_VALUE = {'total': 'total_capacitate', 'start': 'Pornește', 'firmware': 'firmware_VALUE', 'files': 'Fișier_Listă', 'archive_base': 'Arhivă_BASE', 'partition': 'partiție_Fișier', 'archive': 'Arhivă', 'main': 'Pornește', 'block': 'bloc_de_date', 'ROOT': 'Project_rădăcină', 'boot': '부팅경로', 'stage': 'fază_VALUE', 'out': 'KR_date', 'expected': '예상결과', 'f': 'Fișier_intrare', 'src': '원본주소', 'path': 'Cale', 'p': 'date_poziție', 'extracted': '추출자료', 'member': 'membru', 'mbr': 'MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licență', 'source': '원본자료', 'name': 'Nume', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'destinație_VALUE_poziție', 'work': '작업경로'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
