#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'o_lchov_ma_lumotlar', 'build_examples': '예제만들기', 'files': 'fayl_Ro_yxat', 'java': '자바실행', 'run': 'bajarmoq_buyruq', 'path': 'yo_l', 'p': 'ma_lumotlar_holat', 'readme': 'ma_lumot_fayli', 'build_java_library': '자바라이브러리만들기', 'code': 'qo_llanma_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Sinf_yo_l', 'repo': 'repozitoriy_yo_l', 'root': 'ildiz_manzil', 'content': 'tarkib_VALUE', 'source': '원본자료', 'name': 'Nomi', 'target': 'nishon', 'manifest': '꾸러미명세', 'language': 'Til'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
