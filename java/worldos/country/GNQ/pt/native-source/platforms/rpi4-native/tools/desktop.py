#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/desktop_Exibir.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('desktop_Exibir', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('desktop_Exibir')
    mapeamento_VALOR = {'count': 'entrada_CONT_NÚM_8f7753a1', 'special': '특수글쇠', 'error': 'erro', 'exact': 'EXATO_VALOR', 'network': 'rede', 'closed': 'TI_fechado', 'length': 'duração_VALOR', 'opened': '열림', 'ftp_port': 'transferência_de_arquivo_número_da_porta', 'server': 'servidor_VALOR', 'resources': 'Recursos', 'data': 'dados', 'shift': 'tecla_SHIFT', 'send': 'enviar', 'run_desktop': 'executar_desktop', 'protocol': 'rede_ABI', 'forwards': '전달규칙들', 'host': 'host', 'text': 'texto', 'korean': '한글여부', 'port': 'número_da_porta', 'signum': 'sinal_número', 'version': 'número_de_versão', 'parser': 'analisador', 'bridge': 'ponte', 'kind': 'área_VALOR', 'tail': '끝부분', 'size': 'Tamanho', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_coordenada', 'prefix': 'entrelinhamento_bloco', 'client': 'cliente', 'char': 'dados_de_caractere', 'work': '작업경로', 'Keyboard': 'teclado', 'x': 'coordenada_X', 'down': '누르는중', 'net': 'ponte_entrada', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumento_MATRIZ', 'Hangul': '한글조합', 'chunk': 'fragmento_VALOR', 'proc': 'Processo', 'Desktop': 'Conexão_desktop', 'buttons': '단추들', 'thread': 'tarefaSegundoPlano', 'pressed': '눌림', 'previous': 'Anterior', 'toggle': 'mudar_MODO', 'command': 'comando', 'sock': 'soquete_VALOR', 'frame': 'execução_quadro', 'ctrl': 'CTRL', 'path': 'caminho', 'cp': 'codificação_de_caracteres', 'terminate': 'terminar', 'security': 'Segurança', 'vnc_port': '원격화면접속번호', 'body': 'corpo_de_texto', 'index': 'PROC_ÍNDICE', 'exited': '종료됨', 'keysym': 'Chave_símbolo', 'output': 'saída', 'keyboard': 'teclado_entrada', 'interrupted': '가로채기됨', 'listener': 'porta_de_recepção', 'reader': 'Leitor', 'NetworkBridge': 'ponte_3de4fe3a', 'gui': 'desenho_tela', 'worker': 'processamento_Tarefa'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
