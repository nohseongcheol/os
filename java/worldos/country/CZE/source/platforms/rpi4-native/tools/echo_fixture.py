#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/zobrazení_výsledků_testovací_přípravek.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('zobrazení_výsledků_testovací_přípravek', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('zobrazení_výsledků_testovací_přípravek')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'kontakt_e05f319b', 'f': 'Soubor_položka', 'peer': 'partner_HODNOTA', 'self': '자신', 'udp': 'datagram_řízení', 't': 'Terminál_položka', 'tcp': 'kontakt_řízení', 'EchoFixture': 'zobrazení_výsledků_testovací_přípravek', 'args': 'argument_pole', 'chunk': '조각'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
