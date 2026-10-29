#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/개발꾸러미내보내기.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미내보내기')
    대응 = {'out': 'o_lchov_ma_lumotlar', 'obj': 'natijalar_fayli', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arxiv', 'main': 'Bajarish', 'posix': '포직스경로', 'files': 'fayl_Ro_yxat', 'source': '원본자료', 'name': 'Nomi', 'target': 'nishon', 'ROOT': 'Project_ildiz', 'destination': 'ko_chirish_joyi_ma_lumotlar_manzil', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
