#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կառուցել_համակարգ.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կառուցել_համակարգ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կառուցել_համակարգ')
    대응 = {'network': 'Ցանց', 'BUILD': 'կառուցել_ուղի', 'ar': 'Պահոց_գործիք', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'տառատեսակ_տվյալ', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'եղանակ_մուտքագրում', 'main': 'Գործարկել', 'objcopy': 'առարկա_նիշք_փոխարկիչ', 'ROOT': 'արձակել_արմատ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Կերտի_ր_օգտվող_տեղ', 'f': 'նիշք_մուտքագրում', 'extra': '추가영역', 'exports': 'արտահանել_աղյուսակ', 'jobs': '빌드작업', 'run': 'կատարել_հրաման', 'path': 'Ճանապարհ', 'REPO': '저장소', 'tool': 'Գործիքներ', 'classes': 'դաս_ուղի', 'output': '출력결과', 'samples': '예제들', 'symbol': 'նշան_արժեք', 'source': '원본자료', 'name': 'Անուն', 'build_network': 'Կերտի_ր_Ցանց', 'font_info': 'տառատեսակ_տեղեկություն', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
