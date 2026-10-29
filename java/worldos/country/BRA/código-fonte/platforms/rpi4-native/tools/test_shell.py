#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/teste_shell.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('teste_shell', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('teste_shell')
    mapeamento_VALOR = {'timeout': 'execução_TEMPOLIMITE', 'x': 'coordenada_X', 'msg': 'rede_email', 'i': '순번', 'reply': 'resposta', 'call': '호출', 'args': 'argumento_MATRIZ', 'chunk': 'fragmento_VALOR', 'data': 'dados', 'proc': 'Processo', 'long_text': '긴글', 'restored': '복원자료', 'send': 'enviar', 'file': 'ficheiro', 'main': 'iniciar', 'found': 'busca_RC', 'ROOT': 'ação_raiz', 'text': 'texto', 'marker': 'favorito', 'command': 'comando', 'expected': '예상결과', 'pixel': 'pixel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': 'transcrição', 'end': 'encerrar_DESLOC', 'image': 'foto', 'key': '누름값', 'y': 'Y_coordenada', 'output': 'saída', 'result': 'resultado', 'client': 'cliente', 'line': 'linha_de_entrada', 'stream': 'fluxo_VALOR', 'name': 'Nome', 'value': 'VALOR', 'receive': 'receber_email', 'report': 'validação_relatar', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
