#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'үлчәм_мәгълүмат', 'expected': '예상결과', 'phoff': 'кушымта_Башлама_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'дөрес_булмаган_мәгълүмат', 'path': 'Yul', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'үлчәм', 'format_': 'формат_b87fd068', 'main': 'эшләтү', 'content': 'Эчтәлек_VALUE', 'source': '원본자료', 'name': 'исем', 'reference': '비교기준', 'ROOT': 'экранга_җибәрү_тамыр', 'value': 'VALUE', 'report': 'раслау_отчет'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
