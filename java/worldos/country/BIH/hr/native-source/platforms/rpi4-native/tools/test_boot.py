#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'response': 'odgovor_1262b476', 'msg': 'mreža_poruka', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Izvrši', 'cancel': 'Odustani_operacija', 'cmd_byte': 'naredba_bajt', 'reply': 'odgovor', 'points': '지점들', 'server': 'server_VALUE', 'data': 'podaci', 'prompt': 'upit', 'enter': 'unijeti', 'imported': '들여온파일', 'send': 'slati', 'main': 'Pokreni', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'slikovni_element', 'java_class': '자바클래스', 'upload': 'Prijenos_Datoteke', 'pixels_file': 'slikovni_element_Datoteka', 'pixels_data': 'slikovni_element_podaci', 'edit': 'Uredi_VALUE', 'receive_until': '표시까지받기', 'selector': 'odabirač', 'size': 'Veličina', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'REZULTAT', 'samples': '예제들', 'client': 'klijent', 'line': 'red', 'report': 'provjera_izvješće', 'work': '작업경로', 'x': 'koordinata_x', 'python_checks': '파이썬검사', 'download': 'preuzmi', 'greeting': '인사', 'dims': '치수', 'chunk': 'fragment_VALUE', 'deadline': 'rok_za_dovršetak_TIME', 'proc': 'Proces', 'content': 'Sadržaj_VALUE', 'block': 'podatkovni_blok', 'marker': 'marker', 'command': 'Naredba', 'expected': '예상결과', 'shell': 'ljuska', 'drawing': 'crtež_put', 'f': 'Datoteka_unos', 'transcript': 'transkript', 'offset': 'pomak_VALUE', 'path': 'PUTANJA', 'screenshot': 'snimka_zaslona', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'tok_VALUE', 'cmd': '명령인수', 'name': 'Ime', 'qmp': '모의제어접속'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
