#!/usr/bin/env python3
"""기존 पथ 호환 진입점. 실제 구현: ../도구/통신망빌드.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as पथ
체계.path.insert(0, str(पथ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('통신망빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신망빌드')
    대응 = {'obj': '목적파일', 'objects': '목적파일들', 'library': '라이브러리', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': '파일목록', 'source': '원본자료', 'run': '실행', 'flags': '설정비트', 'path': 'पथ', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': '묶음도구'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
