#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    mapare_VALUE = {'out': 'KR_date', 'build_examples': '예제만들기', 'files': 'Fișier_Listă', 'java': '자바실행', 'run': 'executa_comandă', 'path': 'Cale', 'p': 'date_poziție', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'Clasă_cale', 'repo': 'depozit_cale', 'root': 'rădăcină_adresa', 'content': 'Conținut_VALUE', 'source': '원본자료', 'name': 'Nume', 'target': 'țintă', 'manifest': '꾸러미명세', 'language': 'Limbi_străine'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
