#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'ölçü_verilənlər', 'build_examples': '예제만들기', 'files': 'fayl_Siyahı', 'java': '자바실행', 'run': 'icra_etmək_əmr', 'path': 'Cığır', 'p': 'verilənlər_yerinə_qoymaq', 'readme': 'OXUMƏNİ', 'build_java_library': '자바라이브러리만들기', 'code': 'təlimat_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Sinif_yol', 'repo': 'anbar_yol', 'root': 'kök_ünvan', 'content': 'Məzmun_VALUE', 'source': '원본자료', 'name': 'Ad', 'target': 'hədəf', 'manifest': '꾸러미명세', 'language': 'Dil'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
