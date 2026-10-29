#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/예제빌드.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'файл_Спіс', 'java': '자바실행', 'run': 'выканаць_каманда', 'path': 'ШЛЯХ', 'p': '자료위치', 'readme': 'файл_звестак', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'клас_шлях', 'repo': 'рэпазіторый_шлях', 'root': '뿌리주소', 'content': 'кантэнт_значэнне', 'source': '원본자료', 'name': 'Назва', 'target': 'мэтавы_паказчык', 'manifest': '꾸러미명세', 'language': 'Мова'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
