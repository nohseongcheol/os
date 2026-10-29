#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_uživatel_Space.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_uživatel_Space', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_uživatel_Space')
    대응 = {'mode': 'metoda_MODE', 'header': 'Nadpis_HODNOTA', 'i': '순번', 'build_ccompiler': 'Create_C_kompilátor', 'ar': 'Archiv_nástroj', 'posix': '포직스경로', 'payload': 'vytížení_data', 'flags': 'konfigurace_BITS', 'cases': 'testovací_případ', 'cc': 'C_kompilátor', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'linker_nástroj', 'repo': 'úložiště_cesta', 'build_python': 'Create_PYTHON', 'inc': 'zahrnout_cesta', 'argument': '전달값', 'text': 'text', 'headers': 'Nadpis_Seznam', 'cxx': '시플플번역기', 'valid': 'platný', 'build': 'BLD', 'build_users': 'Create_uživatel_Space', 'compiler': 'kompilátor_nástroj', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Nadpis_POSUN', 'offset': 'POSUN_HODNOTA', 'text_address': 'příkaz_ODKAZ', 'abi': 'VOLAT_ABI', 'assembly': 'montáž', 'run': 'Provést_příkaz', 'path': 'cesta_2', 'p': 'data_pozice', 'changed': '바뀐자료', 'n': 'zboží_POČET', 'flag': 'Nastavení_HODNOTA', 'index': 'VYHLEDAT_INDEX', 'classes': 'Třída_cesta', 'output': 'výstup', 'loads': '적재구획', 'data_address': 'data_ODKAZ', 'symbol': 'symbol_HODNOTA', 'root': 'kořen_ODKAZ', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Název', 'value': 'HODNOTA', 'fmt': 'formát_932e03c8', 'work': '작업경로'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
