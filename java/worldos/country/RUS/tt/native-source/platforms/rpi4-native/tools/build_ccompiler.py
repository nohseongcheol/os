#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'үлчәм_мәгълүмат', 'builtins': '내장연산', 'header': 'Башлама_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'үтәргә_команда', 'flags': '설정비트', 'path': 'Yul', 'p': 'мәгълүмат_урнаштыру', 'cc': '시언어번역기', 'obj': 'максат_файл', 'flag': 'Параметрлар_VALUE', 'ld': '연결편집기', 'objects': 'күчерү_урыны_Файллар', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'тамыр_адрес', 'assets': '탑재자료', 'source': '원본자료', 'name': 'исем', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
