#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    vörpun_VALUE = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Net_skeyti', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Keyra', 'cancel': 'Hætta_við_aðgerð', 'cmd_byte': 'skipun_bæti', 'reply': 'svara', 'points': '지점들', 'server': 'þjónn_VALUE', 'data': 'gögn', 'prompt': 'biðja', 'enter': 'slá_inn', 'imported': '들여온파일', 'send': 'senda', 'main': 'Keyra_2', 'ROOT': 'verk_rót', 'text': 'Texti', 'first_gui': '첫화면', 'pixel': 'díll', 'java_class': '자바클래스', 'upload': 'hlaða_upp_Skrár', 'pixels_file': 'díll_skrá', 'pixels_data': 'díll_gögn', 'edit': 'breyta_VALUE', 'receive_until': '표시까지받기', 'selector': 'val', 'size': 'Stærð', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_hnit', 'result': 'NIÐURSTAÐA', 'samples': '예제들', 'client': 'biðlari', 'line': 'Lína', 'report': 'prófun_skrá', 'work': '작업경로', 'x': 'x_hnit', 'python_checks': '파이썬검사', 'download': 'sækja', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Ferli', 'content': 'Efni_VALUE', 'block': 'gögn_útiloka', 'marker': '확인표시', 'command': 'Skipun', 'expected': '예상결과', 'shell': 'skel', 'drawing': 'teikning_slóð', 'f': 'skrá_færsla_3d0c1245', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'SLÓÐ', 'screenshot': 'skjámynd', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'úttak_54cd5e1d', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Heiti', 'qmp': '모의제어접속'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
