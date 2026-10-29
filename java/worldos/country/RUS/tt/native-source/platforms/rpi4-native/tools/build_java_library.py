#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'Башлама_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'төп_өлеш_мәгълүмат', 'src': '원본주소', 'run': 'үтәргә_команда', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'класс_юл', 'dist': '배포경로', 'archive': 'Архив', 'output': '출력결과', 'root': 'тамыр_адрес', 'name': 'исем', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
