#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_sistem.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_sistem')
    preslikava_VALUE = {'network': 'mreža', 'BUILD': 'graditev_pot', 'ar': 'Arhiv_orodje', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'pisava_podatki', 'flags': 'konfiguracija_storitev_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': 'C_prevajalnik', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metoda_vnos', 'main': 'Zaženi', 'objcopy': 'predmet_Datoteka_pretvornik', 'ROOT': 'pobuda_koren', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'prevajalnik_orodje', 'build_users': 'Ustvari_uporabnik_Space', 'f': 'Datoteka_vnos', 'extra': '추가영역', 'exports': 'izvoziti_tabela', 'jobs': '빌드작업', 'run': 'Izvedi_ukaz', 'path': 'POT', 'REPO': 'shramba_koren', 'tool': 'Orodja', 'classes': 'Razred_pot', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Ime', 'build_network': 'Ustvari_mreža', 'font_info': 'pisava_informacije', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
