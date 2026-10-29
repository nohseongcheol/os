#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    vastendamine_VALUE = {'timeout': '시간제한', 'response': 'vastus_1262b476', 'msg': 'võrk_meil', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Käivita', 'cancel': 'Loobu_lõikus', 'cmd_byte': 'käsk_bait', 'reply': 'vastus', 'points': '지점들', 'server': 'server_VALUE', 'data': 'andmed', 'prompt': 'viip', 'enter': 'sisestama', 'imported': '들여온파일', 'send': 'saatma', 'main': 'Käivita_2', 'ROOT': 'Project_juur', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Upload_Failid', 'pixels_file': 'piksel_Fail', 'pixels_data': 'piksel_andmed', 'edit': 'muudatus_VALUE', 'receive_until': '표시까지받기', 'selector': 'valija', 'size': 'Suurus', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'TULEMUS', 'samples': '예제들', 'client': 'klient', 'line': 'Joon', 'report': 'kinnitamine_aruanne', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'alla_laadima', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'tähtaeg_Aeg', 'proc': 'Protsess', 'content': 'Sisu_VALUE', 'block': 'andmeplokk', 'marker': 'marker', 'command': 'Käsk', 'expected': '예상결과', 'shell': 'kest', 'drawing': 'joonis_tee', 'f': 'Fail_kirje', 'transcript': 'transkriptsioon', 'offset': 'nihe_VALUE', 'path': 'RADA', 'screenshot': 'kuvalõige', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'toodang', 'stream': 'voog_VALUE', 'cmd': '명령인수', 'name': 'Nimi_2', 'qmp': '모의제어접속'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
