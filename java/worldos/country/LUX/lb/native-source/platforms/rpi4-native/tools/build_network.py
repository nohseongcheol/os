#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Build_Reseau.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Build_Reseau', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Build_Reseau')
    대응 = {'obj': 'Zilfichier', 'objects': 'Zil_Fichieren', 'library': 'Bibliothéik', 'output': '출력결과', 'port': '접속번호', 'root': 'Racinn_Adress', 'files': 'Fichier_Lëscht', 'source': '원본자료', 'run': 'ausféieren_Befeel', 'flags': '설정비트', 'path': 'Wee', 'build_network': 'Create_Reseau', 'cc': '시언어번역기', 'ar': 'Archiv_Tool'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
