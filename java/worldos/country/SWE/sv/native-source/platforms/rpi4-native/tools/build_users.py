#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_användare_Space.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_användare_Space', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_användare_Space')
    mappning_värde = {'mode': 'metod_läge', 'header': 'huvud_värde', 'i': '순번', 'build_ccompiler': 'Skapa_C_kompilerare', 'ar': 'Arkiv_verktyg', 'posix': '포직스경로', 'payload': 'nyttolast_data', 'flags': 'konfiguration_BITS', 'cases': 'test_akt', 'cc': 'C_kompilerare', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'länkare_verktyg', 'repo': 'centrallager_väg', 'build_python': 'Skapa_PYTHON', 'inc': 'ta_med_väg', 'argument': '전달값', 'text': 'text', 'headers': 'huvud_ange', 'cxx': '시플플번역기', 'valid': 'giltig', 'build': 'version', 'build_users': 'Skapa_användare_Space', 'compiler': 'kompilerare_verktyg', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_huvud_FÖRSKJUTNING', 'offset': 'FÖRSKJUTNING_värde', 'text_address': 'kommando_ADRESS', 'abi': '호출규약', 'assembly': 'montering', 'run': 'köra_kommando', 'path': 'sökväg_2', 'p': 'data_placera', 'changed': '바뀐자료', 'n': 'objekt_ANTAL', 'flag': 'Inställningar_värde', 'index': 'LETAUPP_INDEX', 'classes': 'Kurs_väg', 'output': 'utleverans', 'loads': '적재구획', 'data_address': 'data_ADRESS', 'symbol': 'symbol_värde', 'root': 'rot_ADRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Namn', 'value': 'värde', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
