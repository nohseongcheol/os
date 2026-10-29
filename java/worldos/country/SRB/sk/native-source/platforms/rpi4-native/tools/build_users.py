#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_používateľ_priestor.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_používateľ_priestor', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_používateľ_priestor')
    mapovanie_VALUE = {'mode': 'metóda_MODE', 'header': 'Nadpis_VALUE', 'i': '순번', 'build_ccompiler': 'Create_C_kompilátor', 'ar': 'Archív_nástroj', 'posix': '포직스경로', 'payload': 'údajová_časť_údaje', 'flags': 'konfigurácia_Background_Intelligent_Transfer_Service', 'cases': 'test_prípad', 'cc': 'C_kompilátor', 'data': 'údaje', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'odkladací_priestor_cesta', 'build_python': 'Create_PYTHON', 'inc': 'zahrnúť_cesta', 'argument': '전달값', 'text': 'Spracovanie_textu', 'headers': 'Nadpis_Zoznam', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'zostava_3bf98865', 'build_users': 'Create_používateľ_priestor', 'compiler': 'kompilátor_nástroj', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Nadpis_Posun', 'offset': 'Posun_VALUE', 'text_address': 'príkaz_adresa', 'abi': '호출규약', 'assembly': 'zostava', 'run': 'Vykonať_príkaz', 'path': 'Cesta', 'p': 'údaje_pozícia', 'changed': '바뀐자료', 'n': 'položka_COUNT', 'flag': 'Nastavenia_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'lekcia_cesta', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'údaje_adresa', 'symbol': 'symbol_VALUE', 'root': 'koreň_adresa', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Názov', 'value': 'VALUE', 'fmt': 'formát_932e03c8', 'work': '작업경로'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
