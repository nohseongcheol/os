#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    preslikava_VALUE = {'out': 'KR_podatki', 'build_examples': '예제만들기', 'files': 'Datoteka_Seznam', 'java': '자바실행', 'run': 'Izvedi_ukaz', 'path': 'POT', 'p': 'podatki_položaj', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': 'navodilo_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Razred_pot', 'repo': 'shramba_pot', 'root': 'koren_naslov', 'content': 'vsebina_VALUE', 'source': '원본자료', 'name': 'Ime', 'target': 'tarča', 'manifest': '꾸러미명세', 'language': 'jezik'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
