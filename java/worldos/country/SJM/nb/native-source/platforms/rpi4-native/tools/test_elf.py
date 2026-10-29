#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/실행파일시험.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('실행파일시험')
    tildeling_VERDI = {'out': 'KR_data', 'expected': '예상결과', 'phoff': 'app_Topptekst_FORSKYVNING', 'offset': 'FORSKYVNING_VERDI', 'invalid': 'ugyldig_data', 'path': 'Sti', 'executable': 'kjørbar_fil_BILDE', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'format_b87fd068', 'main': 'Kjør_2', 'content': 'Innhold_VERDI', 'source': '원본자료', 'name': 'Navn', 'reference': 'Sammenligning_grunnlinje', 'ROOT': 'speile_rot', 'value': 'VERDI', 'report': 'validering_rapport'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
