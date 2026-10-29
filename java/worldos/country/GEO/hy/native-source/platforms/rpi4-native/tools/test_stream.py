#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/흐름시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('흐름시험')
    대응 = {'out': 'չափ_տվյալ', 'main': 'Գործարկել', 'ROOT': 'արձակել_արմատ', 'p': 'տվյալ_դիրք', 'text': 'Տեքստ', 'report': 'վավերացում_զեկույց'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
