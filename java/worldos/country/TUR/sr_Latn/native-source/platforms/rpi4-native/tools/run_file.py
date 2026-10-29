#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/Izvrši_Datoteka.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_Datoteka', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_Datoteka')
    mapiranje_VALUE = {'timeout': '시간제한', 's': 'niska_podaci', 'i': '순번', 'match': '일치', 'files': 'Datoteka_Lista', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_niz', 'chunk': '조각', 'data': 'podaci', 'proc': 'Proces', 'send': 'poslati', 'main': 'koristiti', 'marker': 'označivač', 'command': 'komanda', 'include': 'uključiti', 'dumped': '갈무리자료', 'run': 'Izvrši_komanda', 'p': 'podaci_pozicija', 'parser': 'analizator', 'options': 'Opcije', 'kind': 'oblast_VALUE', 'selector': 'birač', 'upload_data': 'Otprema_podaci', 'end': 'završiti_razgovor_Pomak', 'n': 'stavka_COUNT', 'd': 'odredište_podaci', 'key': '누름값', 'output': '출력결과', 'line': 'red', 'name': 'ime', 'upload_name': 'Otprema_ime', 'receive': 'primiti_poruka'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
