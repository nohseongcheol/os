#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_Javanski_navidezni_mehanizem.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_Javanski_navidezni_mehanizem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_Javanski_navidezni_mehanizem')
    preslikava_VALUE = {'message': 'obvestilo_SMS', 's': 'niz_podatki', 'actual': 'dejanski_KR', 'match': '일치', 'payload': 'koristna_vsebina_podatki', 'cases': 'preskusiti_spor', 'fixture': 'preskusiti_podatki', 'main': 'Zaženi', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'valid': '유효함', 'includes': '포함인수', 'include': 'vključevati', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Dokončano_znesek', 'classes': 'Razred_pot', 'output': '출력결과', 'result': 'REZULTAT', 'cmd': '명령인수', 'name': 'Ime', 'jar': '자바꾸러미', 'report': 'preverjanje_veljavnosti_prijavi', 'tests': 'preskusiti_Seznam'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
