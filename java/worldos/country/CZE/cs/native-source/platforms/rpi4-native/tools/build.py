#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_Systém.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_Systém', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_Systém')
    대응 = {'network': 'síť', 'BUILD': 'BLD_cesta', 'ar': 'Archiv_nástroj', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'písmo_data', 'flags': 'konfigurace_BITS', 'a': '첫째값', 'cc': 'C_kompilátor', 'args': 'argument_pole', 'source_flags': '원본설정', 'ld': 'linker_nástroj', 'method': 'metoda_položka', 'main': 'Spustit_2', 'objcopy': 'objekt_Soubor_převaděč', 'ROOT': 'akce_kořen', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilátor_nástroj', 'build_users': 'Create_uživatel_Space', 'f': 'Soubor_položka', 'extra': '추가영역', 'exports': 'exportovat_tabulka', 'jobs': '빌드작업', 'run': 'Provést_příkaz', 'path': 'cesta_2', 'REPO': 'úložiště_kořen', 'tool': 'nástroje', 'classes': 'Třída_cesta', 'output': 'výstup', 'samples': '예제들', 'symbol': 'symbol_HODNOTA', 'source': '원본자료', 'name': 'Název', 'build_network': 'Create_síť', 'font_info': 'písmo_informace', 'manifest': 'sada_manifest', 'work': '작업경로'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
