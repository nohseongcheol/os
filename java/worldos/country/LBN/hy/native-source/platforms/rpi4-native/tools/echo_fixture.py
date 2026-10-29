#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'տվյալ', 'e': '보조항목', 'connection': 'կապ_e05f319b', 'f': 'նիշք_մուտքագրում', 'peer': 'հավասարազոր_սարք_արժեք', 'self': '자신', 'udp': '전문제어', 't': 'Տերմինալ_մուտքագրում', 'tcp': 'կապ_հսկում', 'EchoFixture': '되돌림시험서버', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
