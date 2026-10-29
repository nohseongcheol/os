#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_C_kompajler.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_C_kompajler', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_C_kompajler')
    mapiranje_VALUE = {'out': 'KR_podaci', 'builtins': '내장연산', 'header': 'Zaglavlje_VALUE', 'sdk': 'komplet_za_razvoj_programa', 'build_ccompiler': 'Create_C_kompajler', 'i': '순번', 'elf': '실행파일', 'run': 'Izvrši_komanda', 'flags': 'konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini', 'path': 'putanja', 'p': 'podaci_pozicija', 'cc': 'C_kompajler', 'obj': 'odredišna_datoteka', 'flag': 'Postavke_VALUE', 'ld': '연결편집기', 'objects': 'odredište_Datoteke', 'repo': 'depo_putanja', 'v': '임시값', 'upstream': 'izvorni', 'root': 'koren_adresa', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ime', 'includes': '포함인수'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
