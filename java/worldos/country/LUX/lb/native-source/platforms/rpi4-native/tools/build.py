#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Build_System.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Build_System', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Build_System')
    대응 = {'network': 'Reseau', 'BUILD': 'Build_Wee', 'ar': 'Archiv_Tool', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'Schrëftaart_Daten', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'Argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'Method_Agab', 'main': 'Laf', 'objcopy': 'Objet_Fichier_Konverter', 'ROOT': 'projezéieren_Racinn', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_Benotzer_Plaz', 'f': 'Fichier_Agab', 'extra': '추가영역', 'exports': 'exportéieren_Tabell', 'jobs': '빌드작업', 'run': 'ausféieren_Befeel', 'path': 'Wee', 'REPO': '저장소', 'tool': 'Tools', 'classes': 'Klass_Wee', 'output': '출력결과', 'samples': '예제들', 'symbol': 'Symbol_VALUE', 'source': '원본자료', 'name': 'Numm', 'build_network': 'Create_Reseau', 'font_info': 'Schrëftaart_Info', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
