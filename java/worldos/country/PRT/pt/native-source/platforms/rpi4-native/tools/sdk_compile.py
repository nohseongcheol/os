#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/SDK_compilar.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('SDK_compilar', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('SDK_compilar')
    mapeamento_VALOR = {'compiler': 'compilador_ferramenta', 'obj': 'arquivo_de_destino', 'sdk': 'kit_de_desenvolvimento', 'output': 'saída', 'main': 'iniciar', 'elf': 'executável', 'is_c': 'TI_C_Idioma', 'parser': 'analisador', 'language': 'Idioma', 'work': '작업경로', 'args': 'argumento_MATRIZ'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
