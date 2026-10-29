#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/exekutatu_fitxategi.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('exekutatu_fitxategi', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('exekutatu_fitxategi')
    대응 = {'timeout': '시간제한', 's': 'kate_datuak', 'i': '순번', 'match': '일치', 'files': 'fitxategi_Zerrenda', 'program': 'aplik', 'executable': '실행가능파일', 'args': 'arg_matrize', 'chunk': '조각', 'data': 'datuak', 'proc': 'Prozesua', 'send': 'bidali', 'main': 'Exekutatu_2', 'marker': '확인표시', 'command': 'Komandoa', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'exekutatu_komando', 'p': 'datuak_kargu', 'parser': 'analizatzaile', 'options': 'aukerak', 'kind': 'Kategoria_balio', 'selector': '준비선택기', 'upload_data': 'Upload_datuak', 'end': 'amaitu_Geruzak', 'n': 'elementu_ZENBATU', 'd': 'helburu_datuak', 'key': '누름값', 'output': '출력결과', 'line': 'Marra', 'name': 'Izena', 'upload_name': 'Upload_izen', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
