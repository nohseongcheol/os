#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'forretningsmål_data', 'builtins': '내장연산', 'header': 'hode_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Utfør_kommando', 'flags': '설정비트', 'path': 'STIGE', 'p': 'data_plassere', 'cc': '시언어번역기', 'obj': 'målfil', 'flag': 'Innstillingar_VALUE', 'ld': '연결편집기', 'objects': 'mål_Filer', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'rot_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Namn', 'includes': '포함인수'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
