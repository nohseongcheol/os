#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/부팅시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'resposta_1262b476', 'msg': 'Rede_correo', 'exact': 'EXACTO_VALOR', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Executar', 'cancel': 'Cancelar_cirurxía', 'cmd_byte': 'comando_byte', 'reply': 'resposta', 'points': '지점들', 'server': 'servidor_VALOR', 'data': 'datos', 'prompt': 'avisar', 'enter': 'introducir', 'imported': '들여온파일', 'send': 'enviar', 'main': 'Executar_2', 'ROOT': 'Project_raíz', 'text': 'Texto', 'first_gui': '첫화면', 'pixel': 'píxel', 'java_class': '자바클래스', 'upload': 'carga_Ficheiros', 'pixels_file': 'píxel_Ficheiro', 'pixels_data': 'píxel_datos', 'edit': 'editar_VALOR', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'Tamaño', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEGUNDO_GUI', 'y': 'Y_coordenada', 'result': 'RESULTANTE', 'samples': '예제들', 'client': 'cliente', 'line': 'Liña', 'report': 'validación_informe', 'work': '작업경로', 'x': 'X_coordenada', 'python_checks': '파이썬검사', 'download': 'descarga', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proceso', 'content': 'Contido_VALOR', 'block': 'datos_bloquear', 'marker': '확인표시', 'command': 'Orde', 'expected': '예상결과', 'shell': 'shell', 'drawing': '그림경로', 'f': 'Ficheiro_introdución', 'transcript': '대화기록', 'offset': 'DESPRAZAMENTO_VALOR', 'path': 'CAMIÑO', 'screenshot': 'captura_de_pantalla', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'fluxo_VALOR', 'cmd': '명령인수', 'name': 'Nome', 'qmp': '모의제어접속'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
