#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': 'ɓoggol_keɓe', 'i': '순번', 'match': '일치', 'files': 'fiilde_Doggol', 'program': 'tafirde', 'executable': '실행가능파일', 'args': '인수배열', 'chunk': '조각', 'data': 'keɓe', 'proc': 'Yuɓɓo_golle', 'send': 'neldude', 'main': 'huutoraade', 'marker': '확인표시', 'command': 'ginol', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Cuɓe', 'kind': 'kategorii_njaru', 'selector': '준비선택기', 'upload_data': 'fampaade_keɓe', 'end': '끝위치', 'n': '개수', 'd': 'tiindaare_keɓe', 'key': '누름값', 'output': '출력결과', 'line': 'diidol', 'name': 'innde', 'upload_name': 'fampaade_innde', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
