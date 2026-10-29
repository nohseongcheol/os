#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/teste_desktop.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('teste_desktop', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('teste_desktop')
    mapeamento_VALOR = {'x': 'coordenada_X', 'typing': '글자입력', 'message': 'aviso_SMS', 'start': 'iniciar', 'down': '누르는중', 'exact': 'EXATO_VALOR', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'símbolo', 'j': '안쪽순번', 'deadline': 'data_limite_time', 'proc': 'Processo', 'data': 'dados', 'main': 'iniciar', 'w': '너비값', 'init': '초기값', 'block': 'bloco_de_dados', 'ROOT': 'ação_raiz', 'text': 'texto', 'marker': 'favorito', 'report': 'validação_relatar', 'until': '까지', 'clipboard': 'área_de_transferência_VALOR', 'dst': 'destino_email', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transcrição', 'port': 'número_da_porta', 'offset': 'DESLOC_VALOR', 'h': 'solicitado_altura_VALOR', 'src': '원본주소', 'event': 'Evento', 'encoding': 'conjunto_de_caracteres', 'size': 'Tamanho', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_coordenada', 'output': 'saída', 'symbol': 'símbolo_VALOR', 'client': 'cliente', 'char': 'dados_de_caractere', 'rgb': '빛삼원색'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
