#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_C_kompilator.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_C_kompilator', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_C_kompilator')
    mapiranje_VALUE = {'out': 'KR_podaci', 'builtins': '내장연산', 'header': 'Zaglavlje_VALUE', 'sdk': 'set_razvojnih_alata', 'build_ccompiler': 'Create_C_kompilator', 'i': '순번', 'elf': '실행파일', 'run': 'Izvrši_naredba', 'flags': 'konfiguracija_Pozadinski_pametni_servis_za_transfer', 'path': 'PUTANJA', 'p': 'podaci_položaj', 'cc': 'C_kompilator', 'obj': 'odredišna_datoteka', 'flag': 'Postavke_VALUE', 'ld': '연결편집기', 'objects': 'odredište_Datoteke', 'repo': 'spremište_put', 'v': '임시값', 'upstream': 'koji_ažurira_izvornik', 'root': 'korijen_adresa', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ime', 'includes': '포함인수'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
