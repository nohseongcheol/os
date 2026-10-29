#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_C_prevajalnik.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_C_prevajalnik', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_C_prevajalnik')
    preslikava_VALUE = {'out': 'KR_podatki', 'builtins': '내장연산', 'header': 'Glava_VALUE', 'sdk': 'razvijalski_komplet', 'build_ccompiler': 'Ustvari_C_prevajalnik', 'i': '순번', 'elf': '실행파일', 'run': 'Izvedi_ukaz', 'flags': 'konfiguracija_storitev_Background_Intelligent_Transfer_Service', 'path': 'POT', 'p': 'podatki_položaj', 'cc': 'C_prevajalnik', 'obj': 'ciljna_datoteka', 'flag': 'Nastavitve_VALUE', 'ld': '연결편집기', 'objects': 'cilj_Datoteke', 'repo': 'shramba_pot', 'v': '임시값', 'upstream': 'protitočno', 'root': 'koren_naslov', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ime', 'includes': '포함인수'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
