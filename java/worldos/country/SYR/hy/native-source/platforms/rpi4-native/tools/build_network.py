#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կառուցել_Ցանց.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կառուցել_Ցանց', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կառուցել_Ցանց')
    대응 = {'obj': 'նշանակման_նիշք', 'objects': 'նպատակակետ_Նիշքեր', 'library': 'դարան', 'output': '출력결과', 'port': '접속번호', 'root': 'արմատ_հասցե', 'files': 'նիշք_Ցուցակ', 'source': '원본자료', 'run': 'կատարել_հրաման', 'flags': '설정비트', 'path': 'Ճանապարհ', 'build_network': 'Կերտի_ր_Ցանց', 'cc': '시언어번역기', 'ar': 'Պահոց_գործիք'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
