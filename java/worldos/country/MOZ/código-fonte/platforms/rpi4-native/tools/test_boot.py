#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/부팅시험.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('부팅시험')
    mapeamento_VALOR = {'timeout': 'execução_TEMPOLIMITE', 'response': 'réplica', 'msg': 'rede_email', 'exact': 'EXATO_VALOR', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Executar', 'cancel': 'Close_cirurgia', 'cmd_byte': 'comando_byte', 'reply': 'resposta', 'points': '지점들', 'server': 'servidor_VALOR', 'data': 'dados', 'prompt': 'aviso_1dd14da4', 'enter': 'inserir', 'imported': '들여온파일', 'send': 'enviar', 'main': 'iniciar', 'ROOT': 'ação_raiz', 'text': 'texto', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_Arquivos', 'pixels_file': 'pixel_Arquivo', 'pixels_data': 'pixel_dados', 'edit': 'Editar_VALOR', 'receive_until': '표시까지받기', 'selector': 'seletor', 'size': 'Tamanho', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEGUNDO_GUI', 'y': 'Y_coordenada', 'result': 'resultado', 'samples': '예제들', 'client': 'cliente', 'line': 'linha_de_entrada', 'report': 'validação_relatar', 'work': '작업경로', 'x': 'coordenada_X', 'python_checks': '파이썬검사', 'download': 'baixar', 'greeting': 'saudação_ae353e94', 'dims': '치수', 'chunk': 'fragmento_VALOR', 'deadline': 'data_limite_time', 'proc': 'Processo', 'content': 'Conteúdo_VALOR', 'block': 'bloco_de_dados', 'marker': 'favorito', 'command': 'comando', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'desenho_caminho', 'f': 'Arquivo_entrada', 'transcript': 'transcrição', 'offset': 'DESLOC_VALOR', 'path': 'caminho', 'screenshot': 'captura_de_tela', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'tela_cliente', 'output': 'saída', 'stream': 'fluxo_VALOR', 'cmd': '명령인수', 'name': 'Nome', 'qmp': '모의제어접속'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
