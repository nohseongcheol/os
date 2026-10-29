#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Netwerk_e_pos', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Voer_uit', 'cancel': 'kanselleer_werking', 'cmd_byte': 'bevel_greep', 'reply': 'antwoord', 'points': '지점들', 'server': 'bediener_VALUE', 'data': 'data', 'prompt': 'por', 'enter': 'invoer', 'imported': '들여온파일', 'send': 'e_pos', 'main': 'Loop', 'ROOT': 'Project_wortel', 'text': 'Teks', 'first_gui': '첫화면', 'pixel': 'pieksel', 'java_class': '자바클래스', 'upload': 'oplaai_Lêers', 'pixels_file': 'pieksel_lêer', 'pixels_data': 'pieksel_data', 'edit': 'redigeer_VALUE', 'receive_until': '표시까지받기', 'selector': 'selekteerder', 'size': 'Grootte', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koördinaat', 'result': 'maatreël', 'samples': '예제들', 'client': 'kliënt', 'line': 'lyn', 'report': 'validering_verslag', 'work': '작업경로', 'x': 'x_koördinaat', 'python_checks': '파이썬검사', 'download': 'aflaai', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proses', 'content': 'Inhoud_VALUE', 'block': 'data_blokkeer', 'marker': '확인표시', 'command': 'Opdrag', 'expected': '예상결과', 'shell': 'dop', 'drawing': 'tekening_pad', 'f': 'lêer_inskrywing', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'Pad', 'screenshot': 'skermskoot', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Naam', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
