#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/Izpildīt_Fails.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('Izpildīt_Fails', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izpildīt_Fails')
    kartēšana_VALUE = {'timeout': '시간제한', 's': 'virkne_dati', 'i': '순번', 'match': '일치', 'files': 'Fails_Saraksts', 'program': 'programma', 'executable': 'izpildāms_fails_IMAGE', 'args': 'arg_ARRAY', 'chunk': '조각', 'data': 'dati', 'proc': 'Process', 'send': 'sūtīt', 'main': 'Palaist', 'marker': 'marķieris', 'command': 'Komanda', 'include': 'iekļaut', 'dumped': '갈무리자료', 'run': 'Izpildīt_komanda', 'p': 'dati_amats', 'parser': 'parsētājs', 'options': 'Opcijas', 'kind': 'joma_VALUE', 'selector': 'atlasītājs', 'upload_data': 'Upload_dati', 'end': 'beigt_zvanu_Nobīde', 'n': 'krājums_COUNT', 'd': 'mērķis_dati', 'key': '누름값', 'output': 'ražojums', 'line': 'Līniju', 'name': 'Nosaukums', 'upload_name': 'Upload_nosaukums', 'receive': 'saņemt_ziņa'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
