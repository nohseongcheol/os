#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'Zeechefolleg_Daten', 'actual': 'aktuell_Mooss', 'match': '일치', 'payload': 'nëtzlech_Charge_Daten', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Laf', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'Klass_Wee', 'output': '출력결과', 'result': 'Mooss', 'cmd': '명령인수', 'name': 'Numm', 'jar': '자바꾸러미', 'report': 'Validatioun_mellen', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
