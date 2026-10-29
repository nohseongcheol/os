#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/원격한글시험.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('원격한글시험')
    mapeamento_VALOR = {'wait': '기다리기', 'typing': '글자입력', 'start': 'iniciar', 'profile': 'Perfil', 'focused': 'Destaques', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'servidor_VALOR', 'log': 'LOG_linha', 'args': 'argumento_MATRIZ', 'deadline': 'data_limite_time', 'data': 'dados', 'candidate': 'candidato', 'logs': '기록들', 'kw': 'argumento_nomeado', 'number': '수치', 'main': 'iniciar', 'ready': '준비완료', 'found': 'busca_RC', 'guest': 'convidado', 'ROOT': 'ação_raiz', 'marker': 'favorito', 'text': 'texto', 'out': 'RC_dados', 'env': 'ambiente', 'f': 'Arquivo_entrada', 'port': 'número_da_porta', 'offset': 'DESLOC_VALOR', 'version': 'número_de_versão', 'p': 'dados_cargo', 'selector': 'seletor', 'xvfb': 'virtual_visor', 'display': 'visor', 'n': 'item_CONT_NÚM', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtual_entrada_ferramenta', 'name': 'Nome', 'window': 'Janela', 'report': 'validação_relatar', 'work': '작업경로'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
