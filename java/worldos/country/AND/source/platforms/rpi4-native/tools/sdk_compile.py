#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/개발꾸러미번역.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'fitxer_de_destinació', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Executa_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'analitzador', 'language': 'Idioma', 'work': '작업경로', 'args': 'arg_MATRIU'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
