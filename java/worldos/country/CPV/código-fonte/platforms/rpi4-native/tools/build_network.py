#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/BLD_rede.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_rede', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('BLD_rede')
    mapeamento_VALOR = {'obj': 'arquivo_de_destino', 'objects': 'destino_Arquivos', 'library': 'biblioteca', 'output': 'saída', 'port': 'número_da_porta', 'root': 'raiz_email', 'files': 'lista_de_arquivos', 'source': '원본자료', 'run': 'Executar_comando', 'flags': 'Configuração_BITS', 'path': 'caminho', 'build_network': 'Criar_rede', 'cc': 'C_compilador', 'ar': 'arquivo_ferramenta'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
