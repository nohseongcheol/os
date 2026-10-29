#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_JVM.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_JVM', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_JVM')
    leképezés_ÉRTÉK = {'message': 'alapelv_SMS', 's': 'sztring_adat', 'actual': 'tényleges_KR', 'match': '일치', 'payload': 'teher_adat', 'cases': 'teszt_eset', 'fixture': 'teszt_adat', 'main': 'Futtatás', 'ROOT': 'teendő_gyök', 'text': 'Szöveg', 'valid': 'érvényes', 'includes': '포함인수', 'include': 'tartalmaz', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Kész_összeg', 'classes': 'tanóra_útvonal', 'output': 'kimenet', 'result': 'KR', 'cmd': '명령인수', 'name': 'Név', 'jar': '자바꾸러미', 'report': 'ellenőrzés_jelent', 'tests': 'teszt_Lista'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
