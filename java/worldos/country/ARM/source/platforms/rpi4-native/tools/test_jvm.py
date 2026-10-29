#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/자바가상기계시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'տող_տվյալ', 'actual': 'իրական_չափ', 'match': '일치', 'payload': 'օգտակար_բեռնվածք_տվյալ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Գործարկել', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'դաս_ուղի', 'output': '출력결과', 'result': 'չափ', 'cmd': '명령인수', 'name': 'Անուն', 'jar': '자바꾸러미', 'report': 'վավերացում_զեկույց', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
