#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_Mreža.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_Mreža', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_Mreža')
    mapiranje_VALUE = {'obj': 'odredišna_datoteka', 'objects': 'odredište_Datoteke', 'library': 'biblioteka', 'output': '출력결과', 'port': 'broj_porta', 'root': 'koren_adresa', 'files': 'Datoteka_Lista', 'source': '원본자료', 'run': 'Izvrši_komanda', 'flags': 'konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini', 'path': 'putanja', 'build_network': 'Create_Mreža', 'cc': 'C_kompajler', 'ar': 'Arhiva_alatka'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
