#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/원격한글시험.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Spustit_2', 'profile': 'Profil', 'focused': 'Prioritní', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_HODNOTA', 'log': 'LOGZ_ZÁZNAM', 'args': 'argument_pole', 'deadline': 'konečný_termín_ČAS', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'pojmenovaný_argument', 'number': '수치', 'main': 'Spustit_2', 'ready': '준비완료', 'found': 'HLEDAT_KV', 'guest': 'host', 'ROOT': 'akce_kořen', 'marker': 'značka', 'text': 'text', 'out': 'KV_data', 'env': 'prostředí_5d36e09c', 'f': 'Soubor_položka', 'port': 'číslo_portu', 'offset': 'POSUN_HODNOTA', 'version': 'číslo_verze', 'p': 'data_pozice', 'selector': 'selektor', 'xvfb': 'virtuální_displej', 'display': 'displej', 'n': 'zboží_POČET', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuální_vstup_nástroj', 'name': 'Název', 'window': 'Okno', 'report': 'ověření_Zpráva', 'work': '작업경로'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
