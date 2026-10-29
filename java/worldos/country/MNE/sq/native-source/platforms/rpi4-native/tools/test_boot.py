#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'përgjigje', 'msg': 'rrjet_email', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Kryej', 'cancel': 'Anulo_operim', 'cmd_byte': 'komandë_bajt', 'reply': 'replikë', 'points': '지점들', 'server': 'server_VALUE', 'data': 'të_dhëna', 'prompt': 'kërkoj', 'enter': 'fut', 'imported': '들여온파일', 'send': 'dërgoj', 'main': 'Ekzekuto', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'first_gui': '첫화면', 'pixel': 'pikëz', 'java_class': '자바클래스', 'upload': 'Ngarkim_Skedarët', 'pixels_file': 'pikëz_skedar', 'pixels_data': 'pikëz_të_dhëna', 'edit': 'redaktim_VALUE', 'receive_until': '표시까지받기', 'selector': 'përzgjedhësi', 'size': 'Madhësi', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinatë', 'result': 'llogaritje', 'samples': '예제들', 'client': 'klient', 'line': 'linjë', 'report': 'miratim_raport', 'work': '작업경로', 'x': 'koordinata_x', 'python_checks': '파이썬검사', 'download': 'shkarkim', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proçes', 'content': 'Përmbajtje_VALUE', 'block': 'të_dhëna_bllokoj', 'marker': '확인표시', 'command': 'Komanda', 'expected': '예상결과', 'shell': 'pasues', 'drawing': 'vizatim_shteg', 'f': 'skedar_futje', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'POZICIONI', 'screenshot': 'pamje_e_çastit', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Emër', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
