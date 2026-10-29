#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Create_Bild.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Create_Bild', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_Bild')
    대응 = {'total': '총량', 'start': 'Laf', 'firmware': '기초제어프로그램', 'files': 'Fichier_Lëscht', 'archive_base': 'Archiv_BASE', 'partition': 'Partitioun_Fichier', 'archive': 'Archiv', 'main': 'Laf', 'block': 'Daten_blockéieren', 'ROOT': 'projezéieren_Racinn', 'boot': '부팅경로', 'stage': 'Phas_VALUE', 'out': 'Mooss_Daten', 'expected': '예상결과', 'f': 'Fichier_Agab', 'src': '원본주소', 'path': 'Wee', 'p': 'Daten_positionéieren', 'extracted': '추출자료', 'member': 'Member', 'mbr': '주부트기록', 'image': 'Bild', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lizenzéieren', 'source': '원본자료', 'name': 'Numm', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'Zil_VALUE_positionéieren', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
