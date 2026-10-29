#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/направити_корисник_простор.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('направити_корисник_простор', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('направити_корисник_простор')
    대응 = {'mode': '방식', 'header': 'заглавље_вриједност', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'архива_алатка', 'posix': '포직스경로', 'payload': 'корисни_садржај_подаци', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'подаци', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'текст', 'headers': 'заглавље_списак', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'направити', 'build_users': '사용자영역만들기', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': '프로그램머리변위', 'offset': '변위', 'text_address': 'команда_адреса', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': '실행', 'path': 'пут', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Подешавања_вриједност', 'index': '색인', 'classes': 'класа_пут', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'подаци_адреса', 'symbol': '심볼', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'назив', 'value': 'вриједност', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
