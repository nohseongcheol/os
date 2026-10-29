#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/eraiki_sistema.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('eraiki_sistema', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('eraiki_sistema')
    대응 = {'network': 'sare', 'BUILD': 'eraiki_bide_izen', 'ar': 'artxibo_tresna', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'letra_tipo_datuak', 'flags': 'konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'arg_matrize', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': 'Exekutatu_2', 'objcopy': 'objektu_fitxategi_bihurgailu', 'ROOT': 'Project_erro', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'sortu_erabiltzaile_gune', 'f': 'fitxategi_sarrera', 'extra': '추가영역', 'exports': 'esportatu_taula', 'jobs': '빌드작업', 'run': 'exekutatu_komando', 'path': 'Bide_izena', 'REPO': 'biltegi_erro', 'tool': 'Tresnak', 'classes': 'Gela_bide_izen', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ikur_balio', 'source': '원본자료', 'name': 'Izena', 'build_network': 'sortu_sare', 'font_info': 'letra_tipo_info', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
