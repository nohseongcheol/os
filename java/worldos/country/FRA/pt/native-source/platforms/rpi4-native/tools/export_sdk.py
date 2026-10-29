#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/exportar_SDK.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('exportar_SDK', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('exportar_SDK')
    mapeamento_VALOR = {'out': 'RC_dados', 'obj': 'arquivo_de_destino', 'relative': 'caminho_relativo', 'compiler_archive': 'compilador_arquivo', 'sdk': 'kit_de_desenvolvimento', 'dist': 'distribuição_caminho', 'archive': 'arquivo', 'main': 'iniciar', 'posix': '포직스경로', 'files': 'lista_de_arquivos', 'source': '원본자료', 'name': 'Nome', 'target': 'meta', 'ROOT': 'ação_raiz', 'destination': 'destino_dados_email', 'manifest': 'grupo_manifesto', 'work': '작업경로'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
