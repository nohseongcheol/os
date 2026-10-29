#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_uporabnik_Space.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_uporabnik_Space', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_uporabnik_Space')
    preslikava_VALUE = {'mode': 'metoda_MODE', 'header': 'Glava_VALUE', 'i': '순번', 'build_ccompiler': 'Ustvari_C_prevajalnik', 'ar': 'Arhiv_orodje', 'posix': '포직스경로', 'payload': 'koristna_vsebina_podatki', 'flags': 'konfiguracija_storitev_Background_Intelligent_Transfer_Service', 'cases': 'preskusiti_spor', 'cc': 'C_prevajalnik', 'data': 'podatki', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'shramba_pot', 'build_python': 'Ustvari_PYTHON', 'inc': 'vključevati_pot', 'argument': '전달값', 'text': 'Besedilo', 'headers': 'Glava_Seznam', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'graditev', 'build_users': 'Ustvari_uporabnik_Space', 'compiler': 'prevajalnik_orodje', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'aplikacija_Glava_odmik', 'offset': 'odmik_VALUE', 'text_address': 'ukaz_naslov', 'abi': '호출규약', 'assembly': 'zbir', 'run': 'Izvedi_ukaz', 'path': 'POT', 'p': 'podatki_položaj', 'changed': '바뀐자료', 'n': 'element_COUNT', 'flag': 'Nastavitve_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Razred_pot', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'podatki_naslov', 'symbol': 'simbol_VALUE', 'root': 'koren_naslov', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ime', 'value': 'VALUE', 'fmt': 'oblika_zapisa', 'work': '작업경로'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
