#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'o_lchov_ma_lumotlar', 'builtins': '내장연산', 'header': 'Sarlavha_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'bajarmoq_buyruq', 'flags': 'tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati', 'path': 'yo_l', 'p': 'ma_lumotlar_holat', 'cc': '시언어번역기', 'obj': 'natijalar_fayli', 'flag': 'Sozlamalar_VALUE', 'ld': '연결편집기', 'objects': 'ko_chirish_joyi_Fayllar', 'repo': 'repozitoriy_yo_l', 'v': '임시값', 'upstream': 'yuqorida_turuvchi', 'root': 'ildiz_manzil', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nomi', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
