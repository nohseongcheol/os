#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/코딩시험.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('코딩시험')
    mapeamento_VALOR = {'out': 'RC_dados', 'expected': '예상결과', 'sdk': 'kit_de_desenvolvimento', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'iniciar', 'elf': 'executável', 'run': 'Executar_comando', 'name': 'Nome', 'path': 'caminho', 'p': 'dados_cargo', 'ROOT': 'ação_raiz', 'report': 'validação_relatar', 'args': 'argumento_MATRIZ'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
