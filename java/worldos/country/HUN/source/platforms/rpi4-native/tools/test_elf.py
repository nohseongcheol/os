#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/실행파일시험.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('실행파일시험')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'expected': '예상결과', 'phoff': 'app_fejléc_Ofszet', 'offset': 'Ofszet_ÉRTÉK', 'invalid': 'alaptalan_adat', 'path': 'ÚTVONAL', 'executable': 'végrehajtható_KÉP', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'formáz_b87fd068', 'main': 'Futtatás', 'content': 'Tartalom_ÉRTÉK', 'source': '원본자료', 'name': 'Név', 'reference': 'Összehasonlítás_alap', 'ROOT': 'teendő_gyök', 'value': 'ÉRTÉK', 'report': 'ellenőrzés_jelent'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
