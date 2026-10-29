#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_systém.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_systém', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_systém')
    mapovanie_VALUE = {'network': 'sieť', 'BUILD': 'zostava_cesta', 'ar': 'Archív_nástroj', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'písmo_údaje', 'flags': 'konfigurácia_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': 'C_kompilátor', 'args': 'argument_pole', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metóda_položka', 'main': 'Spustiť_2', 'objcopy': 'objekt_Súbor_konvertor', 'ROOT': 'akcia_koreň', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilátor_nástroj', 'build_users': 'Create_používateľ_priestor', 'f': 'Súbor_položka', 'extra': '추가영역', 'exports': 'exportovať_tabuľka', 'jobs': '빌드작업', 'run': 'Vykonať_príkaz', 'path': 'Cesta', 'REPO': 'odkladací_priestor_koreň', 'tool': 'Nástroje', 'classes': 'lekcia_cesta', 'output': '출력결과', 'samples': '예제들', 'symbol': 'symbol_VALUE', 'source': '원본자료', 'name': 'Názov', 'build_network': 'Create_sieť', 'font_info': 'písmo_informácia', 'manifest': 'zväzok_manifest_zostáv', 'work': '작업경로'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
