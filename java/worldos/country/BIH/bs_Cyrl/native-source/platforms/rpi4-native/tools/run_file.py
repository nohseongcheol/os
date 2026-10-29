#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': 'стринг_подаци', 'i': '순번', 'match': '일치', 'files': 'фајл_списак', 'program': 'програм', 'executable': '실행가능파일', 'args': 'аргумент_низ', 'chunk': '조각', 'data': 'подаци', 'proc': 'процес', 'send': 'послати', 'main': '시작', 'marker': '확인표시', 'command': 'команда', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Опције', 'kind': 'категорија_вриједност', 'selector': '준비선택기', 'upload_data': 'трансферирати_подаци', 'end': '끝위치', 'n': '개수', 'd': 'одредиште_подаци', 'key': '누름값', 'output': '출력결과', 'line': 'редак', 'name': 'назив', 'upload_name': 'трансферирати_назив', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
