#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'չափ_տվյալ', 'builtins': '내장연산', 'header': 'Վերնագիր_արժեք', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'կատարել_հրաման', 'flags': '설정비트', 'path': 'Ճանապարհ', 'p': 'տվյալ_դիրք', 'cc': '시언어번역기', 'obj': 'նշանակման_նիշք', 'flag': 'Կարգավորումներ_արժեք', 'ld': '연결편집기', 'objects': 'նպատակակետ_Նիշքեր', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'արմատ_հասցե', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Անուն', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
