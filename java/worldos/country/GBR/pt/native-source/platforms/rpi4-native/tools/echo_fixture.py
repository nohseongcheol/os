#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/eco_acessório.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('eco_acessório', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('eco_acessório')
    mapeamento_VALOR = {'data': 'dados', 'e': '보조항목', 'connection': 'conexão_e05f319b', 'f': 'Arquivo_entrada', 'peer': 'par_VALOR', 'self': '자신', 'udp': 'datagrama_visual', 't': 'Terminal_entrada', 'tcp': 'conexão_visual', 'EchoFixture': 'eco_acessório', 'args': 'argumento_MATRIZ', 'chunk': 'fragmento_VALOR'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
