#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'Mooss_Daten', 'build_examples': '예제만들기', 'files': 'Fichier_Lëscht', 'java': '자바실행', 'run': 'ausféieren_Befeel', 'path': 'Wee', 'p': 'Daten_positionéieren', 'readme': 'LIESMECH', 'build_java_library': '자바라이브러리만들기', 'code': 'Instruktioun_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Klass_Wee', 'repo': '저장소경로', 'root': 'Racinn_Adress', 'content': 'Inhalt_VALUE', 'source': '원본자료', 'name': 'Numm', 'target': 'Zil', 'manifest': '꾸러미명세', 'language': 'Sprooch'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
