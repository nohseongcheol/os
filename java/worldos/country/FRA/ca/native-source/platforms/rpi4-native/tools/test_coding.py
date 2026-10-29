#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/코딩시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('코딩시험')
    대응 = {'out': 'mesura_dades', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Executa_2', 'elf': '실행파일', 'run': 'Executa_ordre', 'name': 'Nom', 'path': 'Camí', 'p': 'dades_càrrec', 'ROOT': 'Project_rel', 'report': 'validació_informe', 'args': 'arg_MATRIU'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
