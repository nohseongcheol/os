#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/teste_fluxo.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('teste_fluxo', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('teste_fluxo')
    mapeamento_VALOR = {'out': 'RC_dados', 'main': 'iniciar', 'ROOT': 'ação_raiz', 'p': 'dados_cargo', 'text': 'texto', 'report': 'validação_relatar'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
