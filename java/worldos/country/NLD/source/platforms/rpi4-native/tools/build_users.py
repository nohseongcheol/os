#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/build_gebruiker_Space.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('build_gebruiker_Space', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('build_gebruiker_Space')
    toewijzing_WAARDE = {'mode': 'methode_MODUS', 'header': 'header_WAARDE', 'i': '순번', 'build_ccompiler': 'maken_C_compiler', 'ar': 'Archief_hulpmiddel', 'posix': '포직스경로', 'payload': 'payload_gegevens', 'flags': 'configuratie_BITS', 'cases': 'test_case', 'cc': 'C_compiler', 'data': 'gegevens', 'build_java_library': '자바라이브러리만들기', 'ld': 'linker_hulpmiddel', 'repo': 'opslagplaats_pad', 'build_python': 'maken_PYTHON', 'inc': 'bevatten_pad', 'argument': '전달값', 'text': 'tekst', 'headers': 'header_Lijst', 'cxx': '시플플번역기', 'valid': 'geldig', 'build': 'build', 'build_users': 'maken_gebruiker_Space', 'compiler': 'compiler_hulpmiddel', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_header_VERSCHUIVING', 'offset': 'VERSCHUIVING_WAARDE', 'text_address': 'opdracht_ADRES', 'abi': '호출규약', 'assembly': 'assembly', 'run': 'Uitvoeren_opdracht', 'path': 'pad', 'p': 'gegevens_functie', 'changed': '바뀐자료', 'n': 'item_AANTAL', 'flag': 'Instellingen_WAARDE', 'index': 'ZOEKEN_INDEX', 'classes': 'les_pad', 'output': 'uitvoer', 'loads': '적재구획', 'data_address': 'gegevens_ADRES', 'symbol': 'symbool_WAARDE', 'root': 'wortel_ADRES', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Naam', 'value': 'WAARDE', 'fmt': 'indeling', 'work': '작업경로'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
