#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_mreža.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_mreža', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_mreža')
    preslikava_VALUE = {'obj': 'ciljna_datoteka', 'objects': 'cilj_Datoteke', 'library': 'knjižnica', 'output': '출력결과', 'port': 'številka_vrat', 'root': 'koren_naslov', 'files': 'Datoteka_Seznam', 'source': '원본자료', 'run': 'Izvedi_ukaz', 'flags': 'konfiguracija_storitev_Background_Intelligent_Transfer_Service', 'path': 'POT', 'build_network': 'Ustvari_mreža', 'cc': 'C_prevajalnik', 'ar': 'Arhiv_orodje'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
