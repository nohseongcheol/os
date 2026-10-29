#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'Mooss_Daten', 'expected': '예상결과', 'phoff': 'App_En_tête_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'ongëlteg_Daten', 'path': 'Wee', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'Mooss', 'format_': 'Format_b87fd068', 'main': 'Laf', 'content': 'Inhalt_VALUE', 'source': '원본자료', 'name': 'Numm', 'reference': '비교기준', 'ROOT': 'projezéieren_Racinn', 'value': 'VALUE', 'report': 'Validatioun_mellen'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
