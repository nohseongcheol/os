#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/예제빌드.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'չափ_տվյալ', 'build_examples': '예제만들기', 'files': 'նիշք_Ցուցակ', 'java': '자바실행', 'run': 'կատարել_հրաման', 'path': 'Ճանապարհ', 'p': 'տվյալ_դիրք', 'readme': 'ԿԱՐԴԱ_ԻՆՁ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Փնտրում_դասիչ', 'classes': 'դաս_ուղի', 'repo': '저장소경로', 'root': 'արմատ_հասցե', 'content': 'Բովանդակություն_արժեք', 'source': '원본자료', 'name': 'Անուն', 'target': 'թիրախ', 'manifest': '꾸러미명세', 'language': 'Լեզու'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
