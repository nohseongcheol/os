#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/Izvedi_Datoteka.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('Izvedi_Datoteka', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvedi_Datoteka')
    preslikava_VALUE = {'timeout': '시간제한', 's': 'niz_podatki', 'i': '순번', 'match': '일치', 'files': 'Datoteka_Seznam', 'program': 'aplikacija', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'podatki', 'proc': 'Opravilo', 'send': 'poslati', 'main': 'Zaženi', 'marker': 'oznaka', 'command': 'Ukaz', 'include': 'vključevati', 'dumped': '갈무리자료', 'run': 'Izvedi_ukaz', 'p': 'podatki_položaj', 'parser': 'razčlenjevalnik', 'options': 'Možnosti', 'kind': 'območje_VALUE', 'selector': 'izbirnik', 'upload_data': 'Upload_podatki', 'end': 'končati_klic_odmik', 'n': 'element_COUNT', 'd': 'cilj_podatki', 'key': '누름값', 'output': '출력결과', 'line': 'Črtni', 'name': 'Ime', 'upload_name': 'Upload_ime', 'receive': 'sprejeti_sprejemati_prejeti_prejemati_e_pošta'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
