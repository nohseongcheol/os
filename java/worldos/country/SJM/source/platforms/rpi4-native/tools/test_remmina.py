#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/원격한글시험.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('원격한글시험')
    tildeling_VERDI = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Kjør_2', 'profile': 'Profil', 'focused': 'Fokus_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VERDI', 'log': 'LOG_POST', 'args': 'argument_MATRISE', 'deadline': 'tidsfrist_TID', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'navngitt_argument', 'number': '수치', 'main': 'Kjør_2', 'ready': '준비완료', 'found': 'SØK_KR', 'guest': 'gjest', 'ROOT': 'speile_rot', 'marker': 'tusj', 'text': 'Tekst', 'out': 'KR_data', 'env': 'miljø', 'f': 'Fil_oppføring', 'port': 'portnummer', 'offset': 'FORSKYVNING_VERDI', 'version': 'versjonsnummer', 'p': 'data_plassere', 'selector': 'velger', 'xvfb': 'virtuell_vise', 'display': 'skjerm', 'n': 'vare_ANTALL', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuell_inndata_verktøy', 'name': 'Navn', 'window': 'Vindu', 'report': 'validering_rapport', 'work': '작업경로'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
