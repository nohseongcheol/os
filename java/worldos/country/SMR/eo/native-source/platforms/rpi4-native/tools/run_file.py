#!/usr/bin/env python3
"""기존 Vojo 호환 진입점. 실제 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Vojo
체계.path.insert(0, str(Vojo(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': '문자열값', 'i': '순번', 'match': '일치', 'files': '파일목록', 'program': '실행항목', 'executable': '실행가능파일', 'args': '인수배열', 'chunk': '조각', 'data': '자료', 'proc': 'Procezo', 'send': '보내기', 'main': 'Ruli', 'marker': '확인표시', 'command': 'Komando', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': '선택사항', 'kind': '분류', 'selector': '준비선택기', 'upload_data': '올릴자료', 'end': '끝위치', 'n': '개수', 'd': '목적자료', 'key': '누름값', 'output': '출력결과', 'line': 'Linio', 'name': 'Nomo', 'upload_name': '올릴이름', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
