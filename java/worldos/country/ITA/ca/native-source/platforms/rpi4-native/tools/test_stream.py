#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/흐름시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('흐름시험')
    대응 = {'out': 'mesura_dades', 'main': 'Executa_2', 'ROOT': 'Project_rel', 'p': 'dades_càrrec', 'text': 'SMS', 'report': 'validació_informe'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
