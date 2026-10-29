#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/test_Windows.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Windows', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('test_Windows')
    대응 = {'wait': '기다리기', 'x': 'souřadnice_x', 's': 'řetězec_data', 'xy': 'souřadnice', 'sel': 'selektor_a916db4e', 'seconds': '초단위', 'log': 'LOGZ_ZÁZNAM', 'at': 'dobrá_pozice', 'send': 'poslat', 'main': 'Spustit_2', 'req': 'žádost_HODNOTA', 'hot': 'zkratka_HODNOTA', 'pump': 'úchyt_událost', 'ROOT': 'akce_kořen', 'marker': 'značka', 'b': 'SEKUNDA_HODNOTA', 'command': 'příkaz', 'shell': 'prostředí', 'f': 'Soubor_položka', 'color': '색상', 'click': 'klepnout_tlačítko', 'k': '셋째순번', 'c': 'bod_kódu', 'r': '반환값', 'p': 'data_pozice', 'done': 'dokončeno_částka', 'end': 'konec_POSUN', 'command_mode': 'příkaz_MODE', 'key': '누름값', 'y': 'Y_souřadnice', 'pixels': '화소들', 'result': 'VÝSLEDEK', 'report': 'ověření_Zpráva', 'dest': 'cíl_HODNOTA_pozice', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
