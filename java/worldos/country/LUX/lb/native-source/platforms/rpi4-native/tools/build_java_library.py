#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'En_tête_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'nëtzlech_Charge_Daten', 'src': '원본주소', 'run': 'ausféieren_Befeel', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Klass_Wee', 'dist': '배포경로', 'archive': 'Archiv', 'output': '출력결과', 'root': 'Racinn_Adress', 'name': 'Numm', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
