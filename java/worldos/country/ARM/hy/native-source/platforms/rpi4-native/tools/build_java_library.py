#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Վերնագիր_արժեք', 'sources': '원문목록', 'i': '순번', 'info': 'Համակարգի_տեղեկություն', 'payload': 'օգտակար_բեռնվածք_տվյալ', 'src': '원본주소', 'run': 'կատարել_հրաման', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'դաս_ուղի', 'dist': '배포경로', 'archive': 'Պահոց', 'output': '출력결과', 'root': 'արմատ_հասցե', 'name': 'Անուն', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
