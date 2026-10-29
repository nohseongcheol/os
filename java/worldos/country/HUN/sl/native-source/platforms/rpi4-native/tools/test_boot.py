#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    preslikava_VALUE = {'timeout': '시간제한', 'response': 'odziv', 'msg': 'mreža_e_pošta', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Izvedi', 'cancel': 'Prekliči_postopek', 'cmd_byte': 'ukaz_bajt', 'reply': 'odgovor', 'points': '지점들', 'server': 'strežnik_VALUE', 'data': 'podatki', 'prompt': 'poziv', 'enter': 'vnesti', 'imported': '들여온파일', 'send': 'poslati', 'main': 'Zaženi', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'first_gui': '첫화면', 'pixel': 'slikovna_pika', 'java_class': '자바클래스', 'upload': 'Upload_Datoteke', 'pixels_file': 'slikovna_pika_Datoteka', 'pixels_data': 'slikovna_pika_podatki', 'edit': 'Uredi_VALUE', 'receive_until': '표시까지받기', 'selector': 'izbirnik', 'size': 'Velikost', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_grafični_uporabniški_vmesnik', 'y': '세로좌표', 'result': 'REZULTAT', 'samples': '예제들', 'client': 'odjemalec', 'line': 'Črtni', 'report': 'preverjanje_veljavnosti_prijavi', 'work': '작업경로', 'x': 'koordinata_x', 'python_checks': '파이썬검사', 'download': 'prenos', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'rok_čas', 'proc': 'Opravilo', 'content': 'vsebina_VALUE', 'block': 'blok_podatkov', 'marker': 'oznaka', 'command': 'Ukaz', 'expected': '예상결과', 'shell': 'lupina', 'drawing': 'risba_pot', 'f': 'Datoteka_vnos', 'transcript': 'prepis', 'offset': 'odmik_VALUE', 'path': 'POT', 'screenshot': 'izrezek_zaslona', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'tok_VALUE', 'cmd': '명령인수', 'name': 'Ime', 'qmp': '모의제어접속'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
