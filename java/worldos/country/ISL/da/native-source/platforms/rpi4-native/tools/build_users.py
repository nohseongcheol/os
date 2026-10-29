#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_bruger_Space.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_bruger_Space', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_bruger_Space')
    tilknytning_VÆRDI = {'mode': 'metode_HYPPIGST', 'header': 'Header_VÆRDI', 'i': '순번', 'build_ccompiler': 'åbne_C_compiler', 'ar': 'Arkiv_værktøj', 'posix': '포직스경로', 'payload': 'nyttedata_data', 'flags': 'konfiguration_BITS', 'cases': 'test_job', 'cc': 'C_compiler', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'linker_værktøj', 'repo': 'lager_sti', 'build_python': 'åbne_PYTHON', 'inc': 'inkludere_sti', 'argument': '전달값', 'text': 'Tekst', 'headers': 'Header_Liste', 'cxx': '시플플번역기', 'valid': 'gyldig', 'build': 'build', 'build_users': 'åbne_bruger_Space', 'compiler': 'compiler_værktøj', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_Header_FORSKYDNING', 'offset': 'FORSKYDNING_VÆRDI', 'text_address': 'kommando_mail', 'abi': '호출규약', 'assembly': 'montage', 'run': 'Udfør_kommando', 'path': 'Sti', 'p': 'data_placere', 'changed': '바뀐자료', 'n': 'vare_TÆL', 'flag': 'Indstillinger_VÆRDI', 'index': 'Opslag_INDEKS', 'classes': 'Hold_sti', 'output': 'produktoutput', 'loads': '적재구획', 'data_address': 'data_mail', 'symbol': 'symbol_VÆRDI', 'root': 'rod_mail', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Navn', 'value': 'VÆRDI', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
