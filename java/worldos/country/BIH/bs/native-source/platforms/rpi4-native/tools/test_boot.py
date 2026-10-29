#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Mreža_poruka', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Izvrši', 'cancel': 'Otkaži_operacija', 'cmd_byte': 'komanda_bajt', 'reply': 'odgovoriti', 'points': '지점들', 'server': 'server_VALUE', 'data': 'podaci', 'prompt': 'upit', 'enter': 'unijeti', 'imported': '들여온파일', 'send': 'poslati', 'main': 'Pokreni', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'Upload_Fajlovi', 'pixels_file': 'pel_fajl', 'pixels_data': 'pel_podaci', 'edit': 'uređivati_VALUE', 'receive_until': '표시까지받기', 'selector': 'birač', 'size': 'Veličina', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinata', 'result': 'mjera', 'samples': '예제들', 'client': 'klijent', 'line': 'Linija', 'report': 'provjera_izvještaj', 'work': '작업경로', 'x': 'koordinata_x', 'python_checks': '파이썬검사', 'download': 'preuzeti', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'proces', 'content': 'Sadržaj_VALUE', 'block': 'podaci_blokirati', 'marker': '확인표시', 'command': 'Naredba', 'expected': '예상결과', 'shell': 'ljuska', 'drawing': 'ucrtavanje_put', 'f': 'fajl_unos', 'transcript': '대화기록', 'offset': 'Pomak_VALUE', 'path': 'Putanja', 'screenshot': 'snimak_ekrana', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'tok_VALUE', 'cmd': '명령인수', 'name': 'Naziv', 'qmp': '모의제어접속'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
