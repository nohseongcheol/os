#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Reseau_Noriicht', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Ausféieren', 'cancel': 'ofbriechen_Operatioun', 'cmd_byte': 'Befeel_Byte', 'reply': 'äntweren', 'points': '지점들', 'server': 'Server_VALUE', 'data': 'Daten', 'prompt': 'Prompt', 'enter': 'aginn', 'imported': '들여온파일', 'send': 'mailen', 'main': 'Laf', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'Pel', 'java_class': '자바클래스', 'upload': 'eroplueden_Fichieren', 'pixels_file': 'Pel_Fichier', 'pixels_data': 'Pel_Daten', 'edit': 'Editéieren_VALUE', 'receive_until': '표시까지받기', 'selector': 'Selekteur', 'size': 'd_Gréisst_veränneren', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'Mooss', 'samples': '예제들', 'client': 'Client', 'line': 'Zeil', 'report': 'Validatioun_mellen', 'work': '작업경로', 'x': 'X_Koordinat', 'python_checks': '파이썬검사', 'download': 'Download', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Prozess', 'content': 'Inhalt_VALUE', 'block': 'Daten_blockéieren', 'marker': 'Markéierung', 'command': 'Befeel', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'Zeechnung_Wee', 'f': 'Fichier_Agab', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'Wee', 'screenshot': 'Screenshot', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Numm', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
