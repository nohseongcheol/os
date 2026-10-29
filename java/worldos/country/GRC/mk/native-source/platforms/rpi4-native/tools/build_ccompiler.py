#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'мерка_податоци', 'builtins': '내장연산', 'header': 'Заглавие_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Изврши_наредба', 'flags': 'конфигурација_Услуга_за_интелигентен_пренос_во_заднина', 'path': 'ПАТЕКА', 'p': 'податоци_позиционирање', 'cc': '시언어번역기', 'obj': 'одредишна_датотека', 'flag': 'Параметри_VALUE', 'ld': '연결편집기', 'objects': 'одредиште_Датотеки', 'repo': 'склад_патека', 'v': '임시값', 'upstream': 'изворно', 'root': 'корен_адреса', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Име', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
