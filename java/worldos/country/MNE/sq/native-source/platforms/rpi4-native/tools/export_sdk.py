#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/개발꾸러미내보내기.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미내보내기')
    대응 = {'out': 'llogaritje_të_dhëna', 'obj': 'skedari_i_vendmbërritjes', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'arkiv', 'main': 'Ekzekuto', 'posix': '포직스경로', 'files': 'skedar_Listë', 'source': '원본자료', 'name': 'Emër', 'target': 'objektiv', 'ROOT': 'Project_rrënjë', 'destination': 'vendmbërritje_të_dhëna_email', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
