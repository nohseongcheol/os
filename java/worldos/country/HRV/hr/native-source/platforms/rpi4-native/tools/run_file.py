#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/Izvrši_Datoteka.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_Datoteka', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_Datoteka')
    mapiranje_VALUE = {'timeout': '시간제한', 's': 'niz_podaci', 'i': '순번', 'match': '일치', 'files': 'Datoteka_Popis', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': 'fragment_VALUE', 'data': 'podaci', 'proc': 'Proces', 'send': 'slati', 'main': 'Pokreni', 'marker': 'marker', 'command': 'Naredba', 'include': 'obuhvaćati', 'dumped': '갈무리자료', 'run': 'Izvrši_naredba', 'p': 'podaci_položaj', 'parser': 'analizator', 'options': 'Mogućnosti', 'kind': 'područje_VALUE', 'selector': 'odabirač', 'upload_data': 'Prijenos_podaci', 'end': 'završiti_razgovor_pomak', 'n': 'artikl_COUNT', 'd': 'odredište_podaci', 'key': '누름값', 'output': '출력결과', 'line': 'red', 'name': 'Ime', 'upload_name': 'Prijenos_naziv_3f24218e', 'receive': 'primiti_poruka'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
