#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_felhasználó_tér.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_felhasználó_tér', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_felhasználó_tér')
    leképezés_ÉRTÉK = {'mode': 'metódus_mód', 'header': 'fejléc_ÉRTÉK', 'i': '순번', 'build_ccompiler': 'készít_C_fordítóprogram', 'ar': 'archív_eszköz', 'posix': '포직스경로', 'payload': 'teher_adat', 'flags': 'konfiguráció_BITS', 'cases': 'teszt_eset', 'cc': 'C_fordítóprogram', 'data': 'adat', 'build_java_library': '자바라이브러리만들기', 'ld': 'kapcsolószerkesztő_eszköz', 'repo': 'adattár_útvonal', 'build_python': 'készít_PYTHON', 'inc': 'tartalmaz_útvonal', 'argument': '전달값', 'text': 'Szöveg', 'headers': 'fejléc_Lista', 'cxx': '시플플번역기', 'valid': 'érvényes', 'build': 'épít', 'build_users': 'készít_felhasználó_tér', 'compiler': 'fordítóprogram_eszköz', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_fejléc_Ofszet', 'offset': 'Ofszet_ÉRTÉK', 'text_address': 'parancs_CÍM', 'abi': '호출규약', 'assembly': 'szerelvény', 'run': 'végrehajt_parancs', 'path': 'ÚTVONAL', 'p': 'adat_pozíció', 'changed': '바뀐자료', 'n': 'cikk_DARAB', 'flag': 'Gépház_ÉRTÉK', 'index': 'KERES_INDEX', 'classes': 'tanóra_útvonal', 'output': 'kimenet', 'loads': '적재구획', 'data_address': 'adat_CÍM', 'symbol': 'szimbólum_ÉRTÉK', 'root': 'gyök_CÍM', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Név', 'value': 'ÉRTÉK', 'fmt': 'formátum', 'work': '작업경로'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
