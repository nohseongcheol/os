#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/BLD_Terminal_fonte.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_Terminal_fonte', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('BLD_Terminal_fonte')
    mapeamento_VALOR = {'data': 'dados', 'img': 'desenho_VALOR', 'bits': 'BITS_Lista', 'x': 'coordenada_X', 'draw': 'emitir_tela', 'licences': '이용허락목록', 'paths': 'caminho_Lista', 'y': 'Y_coordenada', 'main': 'iniciar', 'src': '원본주소', 'fonts': 'fonte_Lista', 'ROOT': 'ação_raiz', 'p': 'dados_cargo', 'cp': 'codificação_de_caracteres', 'target': 'meta'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
