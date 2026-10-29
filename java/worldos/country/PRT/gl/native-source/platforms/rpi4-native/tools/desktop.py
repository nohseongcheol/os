#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/escritorio_ver.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('escritorio_ver', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('escritorio_ver')
    대응 = {'count': 'introdución_CONTAR', 'special': '특수글쇠', 'error': 'ERRO', 'exact': 'EXACTO_VALOR', 'network': 'Rede', 'closed': '닫힘', 'length': 'duración_VALOR', 'opened': '열림', 'ftp_port': 'transferencia_de_ficheiros_número_do_porto', 'server': 'servidor_VALOR', 'resources': 'Recursos', 'data': 'datos', 'shift': 'tecla_MAIÚS', 'send': 'enviar', 'run_desktop': 'executar_escritorio', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'hospedar', 'text': 'Texto', 'korean': '한글여부', 'port': 'número_do_porto', 'signum': '신호번호', 'version': '판번호', 'parser': 'analizador', 'bridge': 'ponte', 'kind': 'Categoría_VALOR', 'tail': '끝부분', 'size': 'Tamaño', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_coordenada', 'prefix': '앞부분', 'client': 'cliente', 'char': 'carácter_datos', 'work': '작업경로', 'Keyboard': 'teclado', 'x': 'X_coordenada', 'down': '누르는중', 'net': 'Rede_ponte_introdución', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumento_MATRIZ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proceso', 'Desktop': 'CONECTAR_escritorio', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'mudar_MODO', 'command': 'Orde', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'CAMIÑO', 'cp': 'carácter_codificación', 'terminate': '종료시키기', 'security': 'Seguranza', 'vnc_port': '원격화면접속번호', 'body': 'corpo_do_texto', 'index': 'Busca_ÍNDICE', 'exited': '종료됨', 'keysym': 'Chave_símbolo', 'output': '출력결과', 'keyboard': 'teclado_introdución', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Lector', 'NetworkBridge': 'Rede_ponte', 'gui': '그림화면', 'worker': 'procesamento_tarefa'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
