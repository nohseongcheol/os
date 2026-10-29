#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'ölçü_verilənlər', 'builtins': '내장연산', 'header': 'Başlıq_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'icra_etmək_əmr', 'flags': 'konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti', 'path': 'Cığır', 'p': 'verilənlər_yerinə_qoymaq', 'cc': '시언어번역기', 'obj': 'təyinat_faylı', 'flag': 'Parametrlər_VALUE', 'ld': '연결편집기', 'objects': 'təyinat_Fayllar', 'repo': 'anbar_yol', 'v': '임시값', 'upstream': 'mənbə_istiqaməti', 'root': 'kök_ünvan', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ad', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
