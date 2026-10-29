#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_System.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_System', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_System')
    tilknytning_VÆRDI = {'network': 'netværk', 'BUILD': 'build_sti', 'ar': 'Arkiv_værktøj', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'skrifttype_data', 'flags': 'konfiguration_BITS', 'a': '첫째값', 'cc': 'C_compiler', 'args': 'argument_MATRIX', 'source_flags': '원본설정', 'ld': 'linker_værktøj', 'method': 'metode_post', 'main': 'Kør_2', 'objcopy': 'objekt_fil_konverteringsprogram', 'ROOT': 'To_do_rod', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'compiler_værktøj', 'build_users': 'åbne_bruger_Space', 'f': 'fil_post', 'extra': '추가영역', 'exports': 'eksportere_tabel', 'jobs': '빌드작업', 'run': 'Udfør_kommando', 'path': 'Sti', 'REPO': 'lager_rod', 'tool': 'Værktøjer', 'classes': 'Hold_sti', 'output': 'produktoutput', 'samples': '예제들', 'symbol': 'symbol_VÆRDI', 'source': '원본자료', 'name': 'Navn', 'build_network': 'åbne_netværk', 'font_info': 'skrifttype_info', 'manifest': 'bundt_manifest', 'work': '작업경로'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
