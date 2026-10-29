#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'мерка_податоци', 'build_examples': '예제만들기', 'files': 'датотека_Список', 'java': '자바실행', 'run': 'Изврши_наредба', 'path': 'ПАТЕКА', 'p': 'податоци_позиционирање', 'readme': 'информации_пред_употреба', 'build_java_library': '자바라이브러리만들기', 'code': 'инструкција_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'класа_патека', 'repo': 'склад_патека', 'root': 'корен_адреса', 'content': 'Содржина_VALUE', 'source': '원본자료', 'name': 'Име', 'target': 'цел', 'manifest': '꾸러미명세', 'language': 'јазик'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
