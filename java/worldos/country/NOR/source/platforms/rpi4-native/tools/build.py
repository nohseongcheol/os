#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_System.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_System', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_System')
    tildeling_VERDI = {'network': 'nettverk', 'BUILD': 'bygg_bane', 'ar': 'Arkiv_verktøy', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'skrift_data', 'flags': 'konfigurasjon_BITS', 'a': '첫째값', 'cc': 'C_kompilator', 'args': 'argument_MATRISE', 'source_flags': '원본설정', 'ld': 'koblingsprogram_verktøy', 'method': 'metode_oppføring', 'main': 'Kjør_2', 'objcopy': 'objekt_Fil_konverteringsprogram', 'ROOT': 'speile_rot', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilator_verktøy', 'build_users': 'åpne_bruker_Space', 'f': 'Fil_oppføring', 'extra': '추가영역', 'exports': 'eksportere_tabell', 'jobs': '빌드작업', 'run': 'Utfør_kommando', 'path': 'Sti', 'REPO': 'repositorium_rot', 'tool': 'Verktøy', 'classes': 'time_bane', 'output': 'produksjon', 'samples': '예제들', 'symbol': 'symbol_VERDI', 'source': '원본자료', 'name': 'Navn', 'build_network': 'åpne_nettverk', 'font_info': 'skrift_info', 'manifest': 'bunt_manifest', 'work': '작업경로'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
