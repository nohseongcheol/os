#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/Executar_comando.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Executar_comando', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('Executar_comando')
    mapeamento_VALOR = {'supported': '지원목록', 'parser': 'analisador', 'qemu': '모의기계', 'run_desktop': 'executar_desktop', 'main': 'iniciar', 'host': 'host', 'status': 'Estado_VALOR', 'NetworkBridge': 'ponte_3de4fe3a', 'ROOT': 'ação_raiz', 'bridge': 'ponte', 'loader': 'carregador', 'base': 'Tela_de_fundo_VALOR', 'options': 'Opções', 'binary': 'base_2', 'args': 'argumento_MATRIZ', 'command': 'comando'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
