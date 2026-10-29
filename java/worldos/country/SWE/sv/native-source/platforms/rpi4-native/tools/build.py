#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_System.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_System', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_System')
    mappning_värde = {'network': 'nätverk', 'BUILD': 'version_väg', 'ar': 'Arkiv_verktyg', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'teckensnitt_data', 'flags': 'konfiguration_BITS', 'a': '첫째값', 'cc': 'C_kompilerare', 'args': 'argument_MATRIS', 'source_flags': '원본설정', 'ld': 'länkare_verktyg', 'method': 'metod_post', 'main': 'Kör', 'objcopy': 'objekt_fil_konverterare', 'ROOT': 'åtgärd_rot', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilerare_verktyg', 'build_users': 'Skapa_användare_Space', 'f': 'fil_post', 'extra': '추가영역', 'exports': 'exportera_tabell', 'jobs': '빌드작업', 'run': 'köra_kommando', 'path': 'sökväg_2', 'REPO': 'centrallager_rot', 'tool': 'verktyg', 'classes': 'Kurs_väg', 'output': 'utleverans', 'samples': '예제들', 'symbol': 'symbol_värde', 'source': '원본자료', 'name': 'Namn', 'build_network': 'Skapa_nätverk', 'font_info': 'teckensnitt_info', 'manifest': 'bunt_manifest', 'work': '작업경로'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
