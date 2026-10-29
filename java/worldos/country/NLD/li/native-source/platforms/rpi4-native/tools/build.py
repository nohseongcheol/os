#!/usr/bin/env python3
"""기존 Paad 호환 진입점. 실제 구현: ../도구/빌드.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Paad
체계.path.insert(0, str(Paad(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('빌드')
    대응 = {'network': '통신사용', 'BUILD': '빌드경로', 'ar': '묶음도구', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': '글꼴자료', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': '인수배열', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': 'Oetveure', 'objcopy': '목적파일변환기', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': '파일항목', 'extra': '추가영역', 'exports': '공개목록', 'jobs': '빌드작업', 'run': '실행', 'path': 'Paad', 'REPO': '저장소', 'tool': '도구', 'classes': '클래스경로', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': 'Naam', 'build_network': '통신망만들기', 'font_info': '글꼴정보', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
