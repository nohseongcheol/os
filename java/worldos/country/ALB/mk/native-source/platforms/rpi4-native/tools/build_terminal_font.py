#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/верзија_Терминал_фонт.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('верзија_Терминал_фонт', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('верзија_Терминал_фонт')
    대응 = {'data': 'податоци', 'img': 'цртеж_VALUE', 'bits': 'Услуга_за_интелигентен_пренос_во_заднина_Список', 'x': 'координата_х', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'патека_Список', 'y': '세로좌표', 'main': 'Изврши_2', 'src': '원본주소', 'fonts': 'фонт_Список', 'ROOT': 'Project_корен', 'p': 'податоци_позиционирање', 'cp': 'знак_кодирање', 'target': 'цел'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
