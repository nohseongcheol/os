#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/부팅시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'resposta_1262b476', 'msg': 'xarxa_correu', 'exact': 'IGUAL_VALOR', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Executa', 'cancel': 'Cancel_la_cirurgia', 'cmd_byte': 'ordre_byte', 'reply': 'resposta', 'points': '지점들', 'server': 'servidor_VALOR', 'data': 'dades', 'prompt': 'sol_licitar', 'enter': 'introduir', 'imported': '들여온파일', 'send': 'enviar', 'main': 'Executa_2', 'ROOT': 'Project_rel', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'píxel', 'java_class': '자바클래스', 'upload': 'pujar_Fitxers', 'pixels_file': 'píxel_arxiu', 'pixels_data': 'píxel_dades', 'edit': 'Editar_VALOR', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'Mida', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEGON_GUI', 'y': 'Y_coordenada', 'result': 'RESULTAT', 'samples': '예제들', 'client': 'client', 'line': 'línia', 'report': 'validació_informe', 'work': '작업경로', 'x': 'X_coordenada', 'python_checks': '파이썬검사', 'download': 'baixar', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Procés', 'content': 'contingut_VALOR', 'block': 'dades_bloquejar', 'marker': '확인표시', 'command': 'Ordre', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'dibuix_camí', 'f': 'arxiu_introducció', 'transcript': '대화기록', 'offset': 'DESPLAÇAMENT_VALOR', 'path': 'Camí', 'screenshot': 'retall_de_pantalla', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'flux_VALOR', 'cmd': '명령인수', 'name': 'Nom', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
