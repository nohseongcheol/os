#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/BLD_PYTHON.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('BLD_PYTHON')
    mapeamento_VALOR = {'ld': 'vinculador_ferramenta', 'archive': 'arquivo', 'SHA256': 'validação_hash', 'build_python': 'Criar_PYTHON', 'root': 'raiz_email', 'source': '원본자료', 'name': 'Nome', 'path': 'caminho', 'VERSION': 'edição_VALOR', 'cc': 'C_compilador', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'membro'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
