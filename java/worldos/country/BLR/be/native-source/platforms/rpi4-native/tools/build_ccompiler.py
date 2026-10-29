#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'Загаловак_значэнне', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'выканаць_каманда', 'flags': 'канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў', 'path': 'ШЛЯХ', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'канчатковы_файл', 'flag': 'Налады_значэнне', 'ld': '연결편집기', 'objects': 'прызначэнне_Файлы', 'repo': 'рэпазіторый_шлях', 'v': '임시값', 'upstream': 'вышэйстаячы', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Назва', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
