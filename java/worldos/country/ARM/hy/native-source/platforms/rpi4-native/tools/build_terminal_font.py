#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կառուցել_Տերմինալ_տառատեսակ.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կառուցել_Տերմինալ_տառատեսակ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կառուցել_Տերմինալ_տառատեսակ')
    대응 = {'data': 'տվյալ', 'img': 'նկար_արժեք_c143fe9e', 'bits': '비트들', 'x': 'x_կոորդինատ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ուղի_Ցուցակ', 'y': '세로좌표', 'main': 'Գործարկել', 'src': '원본주소', 'fonts': 'տառատեսակ_Ցուցակ', 'ROOT': 'արձակել_արմատ', 'p': 'տվյալ_դիրք', 'cp': 'գրանշան_կոդավորում', 'target': 'թիրախ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
