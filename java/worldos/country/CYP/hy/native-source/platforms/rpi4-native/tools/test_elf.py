#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/실행파일시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'չափ_տվյալ', 'expected': '예상결과', 'phoff': 'ծրագիր_Վերնագիր_Տեղաշարժում', 'offset': 'Տեղաշարժում_արժեք', 'invalid': 'անվավեր_տվյալ', 'path': 'Ճանապարհ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'չափ', 'format_': 'ձեւաչափ_b87fd068', 'main': 'Գործարկել', 'content': 'Բովանդակություն_արժեք', 'source': '원본자료', 'name': 'Անուն', 'reference': '비교기준', 'ROOT': 'արձակել_արմատ', 'value': 'արժեք', 'report': 'վավերացում_զեկույց'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
