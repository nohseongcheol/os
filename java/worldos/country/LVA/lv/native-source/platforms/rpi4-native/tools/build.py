#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_sistēma.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_sistēma', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_sistēma')
    kartēšana_VALUE = {'network': 'tīkls', 'BUILD': 'būvējums_ceļš', 'ar': 'Arhīvs_rīks', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fonts_dati', 'flags': 'konfigurācija_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': 'C_kompilators', 'args': 'arg_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metode_ievade', 'main': 'Palaist', 'objcopy': 'objekts_Fails_pārveidotājs', 'ROOT': 'Project_sakne', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilators_rīks', 'build_users': 'atvērt_lietotājs_telpa', 'f': 'Fails_ievade', 'extra': '추가영역', 'exports': 'eksportēt_tabula', 'jobs': '빌드작업', 'run': 'Izpildīt_komanda', 'path': 'CEĻŠ', 'REPO': 'repozitorijs_sakne', 'tool': 'Rīki', 'classes': 'klase_ceļš', 'output': 'ražojums', 'samples': '예제들', 'symbol': 'simbols_VALUE', 'source': '원본자료', 'name': 'Nosaukums', 'build_network': 'atvērt_tīkls_48d29d6d', 'font_info': 'fonts_informācija', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
