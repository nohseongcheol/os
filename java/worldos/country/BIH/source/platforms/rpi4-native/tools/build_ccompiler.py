#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'заглавље_вриједност', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': '실행', 'flags': '설정비트', 'path': 'пут', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'одредишни_фајл', 'flag': 'Подешавања_вриједност', 'ld': '연결편집기', 'objects': '목적파일들', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'назив', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
