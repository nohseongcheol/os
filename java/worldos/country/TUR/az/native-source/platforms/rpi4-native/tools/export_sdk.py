#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/ixrac_etmək_SDK.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('ixrac_etmək_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ixrac_etmək_SDK')
    대응 = {'out': 'ölçü_verilənlər', 'obj': 'təyinat_faylı', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arxiv', 'main': 'İcra_Et', 'posix': '포직스경로', 'files': 'fayl_Siyahı', 'source': '원본자료', 'name': 'Ad', 'target': 'hədəf', 'ROOT': 'Project_kök', 'destination': 'təyinat_verilənlər_ünvan', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
