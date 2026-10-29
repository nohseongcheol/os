#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_mreža.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_mreža', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_mreža')
    mapiranje_VALUE = {'obj': 'odredišna_datoteka', 'objects': 'odredište_Datoteke', 'library': 'biblioteka', 'output': '출력결과', 'port': 'broj_priključka', 'root': 'korijen_adresa', 'files': 'Datoteka_Popis', 'source': '원본자료', 'run': 'Izvrši_naredba', 'flags': 'konfiguracija_Pozadinski_pametni_servis_za_transfer', 'path': 'PUTANJA', 'build_network': 'Create_mreža', 'cc': 'C_kompilator', 'ar': 'Arhiva_alat'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
