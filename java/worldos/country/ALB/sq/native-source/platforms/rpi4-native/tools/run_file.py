#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/zbatoj_skedar.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('zbatoj_skedar', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zbatoj_skedar')
    대응 = {'timeout': '시간제한', 's': 'varg_të_dhëna', 'i': '순번', 'match': '일치', 'files': 'skedar_Listë', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'të_dhëna', 'proc': 'Proçes', 'send': 'dërgoj', 'main': 'Ekzekuto', 'marker': '확인표시', 'command': 'Komanda', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'zbatoj_komandë', 'p': 'të_dhëna_pozicioni', 'parser': 'analizues', 'options': 'Opsione', 'kind': 'kategori_VALUE', 'selector': 'përzgjedhësi', 'upload_data': 'Ngarkim_të_dhëna', 'end': 'mbaroj_OFFSET', 'n': 'njësi_COUNT', 'd': 'vendmbërritje_të_dhëna', 'key': '누름값', 'output': '출력결과', 'line': 'linjë', 'name': 'Emër', 'upload_name': 'Ngarkim_emër', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
