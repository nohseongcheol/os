#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kurti_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kurti_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kurti_IMAGE')
    susiejimas_VALUE = {'total': 'bendras_pajėgumas', 'start': 'Paleisti', 'firmware': 'programinė_aparatinė_įranga_VALUE', 'files': 'Failas_Sąrašas', 'archive_base': 'Archyvas_BASE', 'partition': 'skaidinys_Failas', 'archive': 'Archyvas', 'main': 'Paleisti', 'block': 'duomenų_blokas', 'ROOT': 'Project_šaknis', 'boot': '부팅경로', 'stage': 'etapas_VALUE', 'out': 'KR_duomenys', 'expected': '예상결과', 'f': 'Failas_įrašas', 'src': '원본주소', 'path': 'KELIAS', 'p': 'duomenys_padėtis', 'extracted': '추출자료', 'member': 'narys', 'mbr': 'MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': 'paskirstymas_kelias', 'sha': '해시계산', 'license_': 'licencija', 'source': '원본자료', 'name': 'Pavadinimas_2', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'vieta_VALUE_padėtis', 'work': '작업경로'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
