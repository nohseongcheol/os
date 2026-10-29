#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'мерка_податоци', 'expected': '예상결과', 'phoff': 'програма_Заглавие_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'неважечки_податоци', 'path': 'ПАТЕКА', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'мерка', 'format_': 'формат_b87fd068', 'main': 'Изврши_2', 'content': 'Содржина_VALUE', 'source': '원본자료', 'name': 'Име', 'reference': 'Споредба_основна_линија', 'ROOT': 'Project_корен', 'value': 'VALUE', 'report': 'проверка_извештај'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
