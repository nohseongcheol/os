#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/Изврши_датотека.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('Изврши_датотека', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Изврши_датотека')
    대응 = {'timeout': '시간제한', 's': 'низа_податоци', 'i': '순번', 'match': '일치', 'files': 'датотека_Список', 'program': 'програма', 'executable': '실행가능파일', 'args': 'аргумент_низа', 'chunk': '조각', 'data': 'податоци', 'proc': 'Процес', 'send': 'испрати', 'main': 'Изврши_2', 'marker': '확인표시', 'command': 'Команда', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Изврши_наредба', 'p': 'податоци_позиционирање', 'parser': 'анализатор', 'options': 'Опции', 'kind': 'област_VALUE', 'selector': 'избирач', 'upload_data': 'постави_податоци', 'end': 'крај_OFFSET', 'n': 'ставка_COUNT', 'd': 'одредиште_податоци', 'key': '누름값', 'output': '출력결과', 'line': 'ред', 'name': 'Име', 'upload_name': 'постави_име', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
