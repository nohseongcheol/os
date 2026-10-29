#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_lietotājs_telpa.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_lietotājs_telpa', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_lietotājs_telpa')
    kartēšana_VALUE = {'mode': 'metode_MODE', 'header': 'galvene_VALUE', 'i': '순번', 'build_ccompiler': 'atvērt_C_kompilators', 'ar': 'Arhīvs_rīks', 'posix': '포직스경로', 'payload': 'vērtums_dati', 'flags': 'konfigurācija_Background_Intelligent_Transfer_Service', 'cases': '시험사례', 'cc': 'C_kompilators', 'data': 'dati', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'repozitorijs_ceļš', 'build_python': 'atvērt_PYTHON', 'inc': 'iekļaut_ceļš', 'argument': '전달값', 'text': 'Teksts', 'headers': 'galvene_Saraksts', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'būvējums', 'build_users': 'atvērt_lietotājs_telpa', 'compiler': 'kompilators_rīks', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programma_galvene_Nobīde', 'offset': 'Nobīde_VALUE', 'text_address': 'komanda_adrese', 'abi': '호출규약', 'assembly': 'montāža', 'run': 'Izpildīt_komanda', 'path': 'CEĻŠ', 'p': 'dati_amats', 'changed': '바뀐자료', 'n': 'krājums_COUNT', 'flag': 'Iestatījumi_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klase_ceļš', 'output': 'ražojums', 'loads': '적재구획', 'data_address': 'dati_adrese', 'symbol': 'simbols_VALUE', 'root': 'sakne_adrese', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nosaukums', 'value': 'VALUE', 'fmt': 'formāts_932e03c8', 'work': '작업경로'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
