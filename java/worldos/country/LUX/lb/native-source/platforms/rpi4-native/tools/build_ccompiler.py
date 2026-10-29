#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'Mooss_Daten', 'builtins': '내장연산', 'header': 'En_tête_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ausféieren_Befeel', 'flags': '설정비트', 'path': 'Wee', 'p': 'Daten_positionéieren', 'cc': '시언어번역기', 'obj': 'Zilfichier', 'flag': 'Astellungen_VALUE', 'ld': '연결편집기', 'objects': 'Zil_Fichieren', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'Racinn_Adress', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Numm', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
