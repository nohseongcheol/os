#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/կառուցել_օգտվող_տեղ.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('կառուցել_օգտվող_տեղ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('կառուցել_օգտվող_տեղ')
    대응 = {'mode': 'եղանակ_կերպ', 'header': 'Վերնագիր_արժեք', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Պահոց_գործիք', 'posix': '포직스경로', 'payload': 'օգտակար_բեռնվածք_տվյալ', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'տվյալ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Տեքստ', 'headers': 'Վերնագիր_Ցուցակ', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'կառուցել', 'build_users': 'Կերտի_ր_օգտվող_տեղ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ծրագիր_Վերնագիր_Տեղաշարժում', 'offset': 'Տեղաշարժում_արժեք', 'text_address': 'հրաման_հասցե', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'կատարել_հրաման', 'path': 'Ճանապարհ', 'p': 'տվյալ_դիրք', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Կարգավորումներ_արժեք', 'index': 'Փնտրում_դասիչ', 'classes': 'դաս_ուղի', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'տվյալ_հասցե', 'symbol': 'նշան_արժեք', 'root': 'արմատ_հասցե', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Անուն', 'value': 'արժեք', 'fmt': 'ձեւաչափ_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
