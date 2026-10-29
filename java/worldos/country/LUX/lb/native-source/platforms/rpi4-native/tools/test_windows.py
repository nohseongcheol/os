#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/창시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'X_Koordinat', 's': 'Zeechefolleg_Daten', 'xy': 'Koordinatekoppel', 'sel': 'Selekteur_a916db4e', 'seconds': '초단위', 'log': 'LOG_Rei', 'at': '현재위치', 'send': 'mailen', 'main': 'Laf', 'req': '요청값', 'hot': 'Ofkierzung_VALUE', 'pump': 'Handle_Evenement', 'ROOT': 'projezéieren_Racinn', 'marker': 'Markéierung', 'b': 'SECOND_VALUE', 'command': 'Befeel', 'shell': 'Shell', 'f': 'Fichier_Agab', 'color': '색상', 'click': 'klicken_Tast', 'k': '셋째순번', 'c': 'Zeechecode', 'r': '반환값', 'p': 'Daten_positionéieren', 'done': '완료량', 'end': 'bëennegen_OFFSET', 'command_mode': 'Befeel_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'Mooss', 'report': 'Validatioun_mellen', 'dest': 'Zil_VALUE_positionéieren', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
