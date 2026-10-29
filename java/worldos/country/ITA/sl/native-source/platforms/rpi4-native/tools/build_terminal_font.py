#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_Terminal_pisava.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_Terminal_pisava', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_Terminal_pisava')
    preslikava_VALUE = {'data': 'podatki', 'img': 'risba_VALUE', 'bits': 'storitev_Background_Intelligent_Transfer_Service_Seznam', 'x': 'koordinata_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'pot_Seznam', 'y': '세로좌표', 'main': 'Zaženi', 'src': '원본주소', 'fonts': 'pisava_Seznam', 'ROOT': 'pobuda_koren', 'p': 'podatki_položaj', 'cp': 'kodiranje_znakov', 'target': 'tarča'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
