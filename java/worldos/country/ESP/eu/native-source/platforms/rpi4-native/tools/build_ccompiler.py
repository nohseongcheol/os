#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/시언어번역기빌드.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('시언어번역기빌드')
    대응 = {'out': 'neurria_datuak', 'builtins': '내장연산', 'header': 'goiburu_balio', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'exekutatu_komando', 'flags': 'konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna', 'path': 'Bide_izena', 'p': 'datuak_kargu', 'cc': '시언어번역기', 'obj': 'helburuko_fitxategi', 'flag': 'Ezarpenak_balio', 'ld': '연결편집기', 'objects': 'helburu_Fitxategiak', 'repo': 'biltegi_bide_izen', 'v': '임시값', 'upstream': 'goranzko', 'root': 'erro_helbide', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Izena', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
