#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կատարել_հրաման.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կատարել_հրաման', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կատարել_հրաման')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'աշխատեցնել_սեղան', 'main': 'Գործարկել', 'host': 'հոստ', 'status': 'վիճակ_արժեք', 'NetworkBridge': 'Ցանց_կամուրջ', 'ROOT': 'արձակել_արմատ', 'bridge': 'կամուրջ', 'loader': '적재기', 'base': 'խորք_արժեք', 'options': 'Ընտրանքներ', 'binary': 'երկուական', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'command': 'Հրահանգ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
