#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կատարել_նիշք.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կատարել_նիշք', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կատարել_նիշք')
    대응 = {'timeout': '시간제한', 's': 'տող_տվյալ', 'i': '순번', 'match': '일치', 'files': 'նիշք_Ցուցակ', 'program': 'ծրագիր', 'executable': '실행가능파일', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'chunk': '조각', 'data': 'տվյալ', 'proc': 'Գործընթաց', 'send': 'ուղարկել', 'main': 'Գործարկել', 'marker': '확인표시', 'command': 'Հրահանգ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'կատարել_հրաման', 'p': 'տվյալ_դիրք', 'parser': '인수해석기', 'options': 'Ընտրանքներ', 'kind': 'անվանակարգ_արժեք', 'selector': 'ընտրիչ', 'upload_data': 'վերբեռնել_տվյալ', 'end': 'վերջացնել_Տեղաշարժում', 'n': '개수', 'd': 'նպատակակետ_տվյալ', 'key': '누름값', 'output': '출력결과', 'line': 'կապ', 'name': 'Անուն', 'upload_name': 'վերբեռնել_անուն', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
