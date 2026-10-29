#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    mapovanie_VALUE = {'total': 'celkovo_kapacita', 'start': 'Spustiť_2', 'firmware': 'firmvér_VALUE', 'files': 'Súbor_Zoznam', 'archive_base': 'Archív_BASE', 'partition': 'oblasť_Súbor', 'archive': 'Archív', 'main': 'Spustiť_2', 'block': 'blok_údajov', 'ROOT': 'akcia_koreň', 'boot': '부팅경로', 'stage': 'etapa_VALUE', 'out': 'KR_údaje', 'expected': '예상결과', 'f': 'Súbor_položka', 'src': '원본주소', 'path': 'Cesta', 'p': 'údaje_pozícia', 'extracted': '추출자료', 'member': 'člen', 'mbr': 'hlavný_zavádzací_záznam', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licencia', 'source': '원본자료', 'name': 'Názov', 'value': 'VALUE', 'manifest': 'zväzok_manifest_zostáv', 'dest': 'cieľ_VALUE_pozícia', 'work': '작업경로'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
