#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/Ustvari_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('Ustvari_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Ustvari_IMAGE')
    preslikava_VALUE = {'total': 'skupaj_zmogljivost', 'start': 'Zaženi', 'firmware': 'vdelana_programska_oprema_VALUE', 'files': 'Datoteka_Seznam', 'archive_base': 'Arhiv_BASE', 'partition': 'particija_Datoteka', 'archive': 'Arhiv', 'main': 'Zaženi', 'block': 'blok_podatkov', 'ROOT': 'pobuda_koren', 'boot': '부팅경로', 'stage': 'območje_VALUE_29ee1bb7', 'out': 'KR_podatki', 'expected': '예상결과', 'f': 'Datoteka_vnos', 'src': '원본주소', 'path': 'POT', 'p': 'podatki_položaj', 'extracted': '추출자료', 'member': 'član', 'mbr': 'sektor_MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licenca', 'source': '원본자료', 'name': 'Ime', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'cilj_VALUE_položaj', 'work': '작업경로'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
