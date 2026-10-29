#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Nettverk_melding', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Køyr', 'cancel': 'Avbryt_operasjon', 'cmd_byte': 'kommando_byte', 'reply': 'svare', 'points': '지점들', 'server': 'tenar_VALUE', 'data': 'data', 'prompt': 'spørsmål', 'enter': 'skrive_inn', 'imported': '들여온파일', 'send': 'sende', 'main': 'Køyr_2', 'ROOT': 'spegle_rot', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Upload_Filer', 'pixels_file': 'piksel_fil', 'pixels_data': 'piksel_data', 'edit': 'redigere_VALUE', 'receive_until': '표시까지받기', 'selector': 'veljar', 'size': 'Storleik', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinat', 'result': 'forretningsmål', 'samples': '예제들', 'client': 'klient', 'line': 'linje', 'report': 'validering_rapport', 'work': '작업경로', 'x': 'x_koordinat', 'python_checks': '파이썬검사', 'download': 'laste_ned', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Prosess', 'content': 'Innhald_VALUE', 'block': 'data_Blokker', 'marker': '확인표시', 'command': 'Kommando', 'expected': '예상결과', 'shell': 'grensesnitt', 'drawing': 'teikning_bane', 'f': 'fil_oppføring', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'STIGE', 'screenshot': 'skjermbilete', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Namn', 'qmp': '모의제어접속'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
