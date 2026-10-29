#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/teste_Windows.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('teste_Windows', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('teste_Windows')
    mapeamento_VALOR = {'wait': '기다리기', 'x': 'coordenada_X', 's': 'cadeia_dados', 'xy': 'par_de_coordenadas', 'sel': 'seletor_a916db4e', 'seconds': '초단위', 'log': 'LOG_linha', 'at': 'em_dia_cargo', 'send': 'enviar', 'main': 'iniciar', 'req': 'solicitação_VALOR', 'hot': 'atalho_VALOR', 'pump': 'alça_Evento', 'ROOT': 'ação_raiz', 'marker': 'favorito', 'b': 'SEGUNDO_VALOR', 'command': 'comando', 'shell': 'shell', 'f': 'Arquivo_entrada', 'color': '색상', 'click': 'clicar_botão', 'k': '셋째순번', 'c': 'ponto_de_código', 'r': '반환값', 'p': 'dados_cargo', 'done': 'concluído_valor', 'end': 'encerrar_DESLOC', 'command_mode': 'comando_MODO', 'key': '누름값', 'y': 'Y_coordenada', 'pixels': '화소들', 'result': 'resultado', 'report': 'validação_relatar', 'dest': 'destino_VALOR_cargo', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
