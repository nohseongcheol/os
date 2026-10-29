#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/실행파일시험.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('실행파일시험')
    tilknytning_VÆRDI = {'out': 'KR_data', 'expected': '예상결과', 'phoff': 'app_Header_FORSKYDNING', 'offset': 'FORSKYDNING_VÆRDI', 'invalid': 'ugyldig_data', 'path': 'Sti', 'executable': 'eksekverbar_fil_Image', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'format_b87fd068', 'main': 'Kør_2', 'content': 'Indhold_VÆRDI', 'source': '원본자료', 'name': 'Navn', 'reference': 'Sammenligning_baseline', 'ROOT': 'To_do_rod', 'value': 'VÆRDI', 'report': 'validering_rapport'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
