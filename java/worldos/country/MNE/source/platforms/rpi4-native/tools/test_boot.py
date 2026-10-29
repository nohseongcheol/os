#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'response': 'odgovor_1262b476', 'msg': 'Mreža_poruka', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Izvrši_obaveza', 'cancel': 'Otkaži_operacija', 'cmd_byte': 'komanda_bajt', 'reply': 'odgovor', 'points': '지점들', 'server': 'server_VALUE', 'data': 'podaci', 'prompt': 'odziv', 'enter': 'uneti', 'imported': '들여온파일', 'send': 'poslati', 'main': 'koristiti', 'ROOT': 'radnja_koren', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Otprema_Datoteke', 'pixels_file': 'piksel_Datoteka', 'pixels_data': 'piksel_podaci', 'edit': 'Uredi_VALUE', 'receive_until': '표시까지받기', 'selector': 'birač', 'size': 'promeniti_veličinu', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'KR', 'samples': '예제들', 'client': 'klijent', 'line': 'red', 'report': 'provera_valjanosti_izveštaj', 'work': '작업경로', 'x': 'x_koordinata', 'python_checks': '파이썬검사', 'download': 'preuzmi', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'krajnji_rok_TIME', 'proc': 'Proces', 'content': 'Sadržaj_VALUE', 'block': 'blok_podataka', 'marker': 'označivač', 'command': 'komanda', 'expected': '예상결과', 'shell': 'ljuska', 'drawing': 'crtež_putanja', 'f': 'Datoteka_stavka', 'transcript': 'transkript', 'offset': 'Pomak_VALUE', 'path': 'putanja', 'screenshot': 'isečak_ekrana', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'tok_VALUE', 'cmd': '명령인수', 'name': 'ime', 'qmp': '모의제어접속'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
