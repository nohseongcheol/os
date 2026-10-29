#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/készít_KÉP.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('készít_KÉP', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('készít_KÉP')
    leképezés_ÉRTÉK = {'total': 'összesen_kapacitás', 'start': 'Futtatás', 'firmware': '기초제어프로그램', 'files': 'fájllista', 'archive_base': 'archív_ALAP', 'partition': 'partíció_Fájl', 'archive': 'archív', 'main': 'Futtatás', 'block': 'adatblokk', 'ROOT': 'teendő_gyök', 'boot': '부팅경로', 'stage': 'fázis_ÉRTÉK', 'out': 'KR_adat', 'expected': '예상결과', 'f': 'Fájl_bejegyzés', 'src': '원본주소', 'path': 'ÚTVONAL', 'p': 'adat_pozíció', 'extracted': '추출자료', 'member': 'tag', 'mbr': 'MBR', 'image': 'KÉP', 'sector_count': '섹터개수', 'dist': 'elosztás_útvonal', 'sha': '해시계산', 'license_': 'licenc', 'source': '원본자료', 'name': 'Név', 'value': 'ÉRTÉK', 'manifest': 'köteg_jegyzékfájl', 'dest': 'cél_ÉRTÉK_pozíció', 'work': '작업경로'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
