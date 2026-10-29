#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/направити_систем.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('направити_систем', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('направити_систем')
    대응 = {'network': 'Мрежа', 'BUILD': 'направити_пут', 'ar': 'архива_алатка', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'фонт_подаци', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_низ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': '시작', 'objcopy': 'објект_фајл_претварач', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'фајл_унос', 'extra': '추가영역', 'exports': 'извозити_табела', 'jobs': '빌드작업', 'run': '실행', 'path': 'пут', 'REPO': '저장소', 'tool': '도구', 'classes': 'класа_пут', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': 'назив', 'build_network': '통신망만들기', 'font_info': 'фонт_информација', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
