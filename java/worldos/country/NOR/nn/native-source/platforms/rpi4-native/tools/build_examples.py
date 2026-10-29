#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'forretningsmål_data', 'build_examples': '예제만들기', 'files': 'fil_Liste', 'java': '자바실행', 'run': 'Utfør_kommando', 'path': 'STIGE', 'p': 'data_plassere', 'readme': 'Viktig', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksjon_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'time_bane', 'repo': '저장소경로', 'root': 'rot_ADDRESS', 'content': 'Innhald_VALUE', 'source': '원본자료', 'name': 'Namn', 'target': 'mål', 'manifest': '꾸러미명세', 'language': 'Språk'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
