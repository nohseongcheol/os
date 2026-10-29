#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/ausféieren_Fichier.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('ausféieren_Fichier', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ausféieren_Fichier')
    대응 = {'timeout': '시간제한', 's': 'Zeechefolleg_Daten', 'i': '순번', 'match': '일치', 'files': 'Fichier_Lëscht', 'program': 'App', 'executable': '실행가능파일', 'args': 'Argument_ARRAY', 'chunk': '조각', 'data': 'Daten', 'proc': 'Prozess', 'send': 'mailen', 'main': 'Laf', 'marker': 'Markéierung', 'command': 'Befeel', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ausféieren_Befeel', 'p': 'Daten_positionéieren', 'parser': '인수해석기', 'options': 'Optiounen', 'kind': 'Kategorie_VALUE', 'selector': 'Selekteur', 'upload_data': 'eroplueden_Daten', 'end': 'bëennegen_OFFSET', 'n': 'Element_COUNT', 'd': 'Zil_Daten', 'key': '누름값', 'output': '출력결과', 'line': 'Zeil', 'name': 'Numm', 'upload_name': 'eroplueden_Numm', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
