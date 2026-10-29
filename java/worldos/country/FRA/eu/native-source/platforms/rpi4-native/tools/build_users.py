#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/eraiki_erabiltzaile_gune.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('eraiki_erabiltzaile_gune', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('eraiki_erabiltzaile_gune')
    대응 = {'mode': '방식', 'header': 'goiburu_balio', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'artxibo_tresna', 'posix': '포직스경로', 'payload': 'karga_datuak', 'flags': 'konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'datuak', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'biltegi_bide_izen', 'build_python': 'sortu_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Testua', 'headers': 'goiburu_Zerrenda', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'eraiki', 'build_users': 'sortu_erabiltzaile_gune', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'aplik_goiburu_Geruzak', 'offset': 'Geruzak_balio', 'text_address': 'komando_helbide', 'abi': '호출규약', 'assembly': 'mihiztatze', 'run': 'exekutatu_komando', 'path': 'Bide_izena', 'p': 'datuak_kargu', 'changed': '바뀐자료', 'n': 'elementu_ZENBATU', 'flag': 'Ezarpenak_balio', 'index': 'BEGIRATU_INDIZE', 'classes': 'Gela_bide_izen', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'datuak_helbide', 'symbol': 'ikur_balio', 'root': 'erro_helbide', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Izena', 'value': 'balio', 'fmt': 'formatu_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
