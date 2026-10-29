#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/SDK_bangun.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('SDK_bangun', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('SDK_bangun')
    대응 = {'compiler': '번역기', 'obj': 'file_tujuan', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'jalankan', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'parser', 'language': 'Bahasa', 'work': '작업경로', 'args': 'argumen_ARRAY'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
