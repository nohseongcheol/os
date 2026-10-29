#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/bouwen.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('bouwen', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('bouwen')
    toewijzing_WAARDE = {'network': 'net', 'BUILD': 'build_pad', 'ar': 'Archief_hulpmiddel', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'lettertype_gegevens', 'flags': 'configuratie_BITS', 'a': '첫째값', 'cc': 'C_compiler', 'args': 'argument_MATRIX', 'source_flags': '원본설정', 'ld': 'linker_hulpmiddel', 'method': 'methode_invoer', 'main': 'starten', 'objcopy': 'object_Bestand_conversieprogramma', 'ROOT': 'Taken_wortel', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'compiler_hulpmiddel', 'build_users': 'maken_gebruiker_Space', 'f': 'Bestand_invoer', 'extra': '추가영역', 'exports': 'exporteren_tabel', 'jobs': '빌드작업', 'run': 'Uitvoeren_opdracht', 'path': 'pad', 'REPO': 'opslagplaats_wortel', 'tool': 'hulpmiddelen', 'classes': 'les_pad', 'output': 'uitvoer', 'samples': '예제들', 'symbol': 'symbool_WAARDE', 'source': '원본자료', 'name': 'Naam', 'build_network': 'maken_net', 'font_info': 'lettertype_info', 'manifest': 'bundel_manifest', 'work': '작업경로'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
