#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_bruker_Space.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_bruker_Space', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_bruker_Space')
    tildeling_VERDI = {'mode': 'metode_MODUS', 'header': 'Topptekst_VERDI', 'i': '순번', 'build_ccompiler': 'åpne_C_kompilator', 'ar': 'Arkiv_verktøy', 'posix': '포직스경로', 'payload': 'nyttelast_data', 'flags': 'konfigurasjon_BITS', 'cases': 'test_sak', 'cc': 'C_kompilator', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'koblingsprogram_verktøy', 'repo': 'repositorium_bane', 'build_python': 'åpne_PYTHON', 'inc': 'inkludere_bane', 'argument': '전달값', 'text': 'Tekst', 'headers': 'Topptekst_Liste', 'cxx': '시플플번역기', 'valid': 'gyldig', 'build': 'bygg', 'build_users': 'åpne_bruker_Space', 'compiler': 'kompilator_verktøy', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_Topptekst_FORSKYVNING', 'offset': 'FORSKYVNING_VERDI', 'text_address': 'kommando_e_post', 'abi': '호출규약', 'assembly': 'samling', 'run': 'Utfør_kommando', 'path': 'Sti', 'p': 'data_plassere', 'changed': '바뀐자료', 'n': 'vare_ANTALL', 'flag': 'Innstillinger_VERDI', 'index': 'Oppslag_INDEKS', 'classes': 'time_bane', 'output': 'produksjon', 'loads': '적재구획', 'data_address': 'data_e_post', 'symbol': 'symbol_VERDI', 'root': 'rot_e_post', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Navn', 'value': 'VERDI', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
