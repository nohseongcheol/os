#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/원격한글시험.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('원격한글시험')
    leképezés_ÉRTÉK = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Futtatás', 'profile': 'Profil', 'focused': 'Szűrt', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'kiszolgáló_ÉRTÉK', 'log': 'LOG_REKORD', 'args': 'argumentum_TÖMB', 'deadline': 'határidő_IDŐ', 'data': 'adat', 'candidate': '후보', 'logs': '기록들', 'kw': 'megnevezett_argumentum', 'number': '수치', 'main': 'Futtatás', 'ready': '준비완료', 'found': 'keres_KR', 'guest': 'vendég', 'ROOT': 'teendő_gyök', 'marker': 'jelölő', 'text': 'Szöveg', 'out': 'KR_adat', 'env': 'környezet_5d36e09c', 'f': 'Fájl_bejegyzés', 'port': 'portszám', 'offset': 'Ofszet_ÉRTÉK', 'version': 'verziószám', 'p': 'adat_pozíció', 'selector': 'szelektor', 'xvfb': 'virtuális_kijelző', 'display': 'kijelző', 'n': 'cikk_DARAB', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuális_bevitel_eszköz', 'name': 'Név', 'window': 'Ablak', 'report': 'ellenőrzés_jelent', 'work': '작업경로'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
