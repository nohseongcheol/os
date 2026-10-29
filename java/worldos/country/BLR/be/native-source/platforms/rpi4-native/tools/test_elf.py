#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/실행파일시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'праграма_Загаловак_Зрух', 'offset': 'Зрух_значэнне', 'invalid': 'памылковы_дадзеныя', 'path': 'ШЛЯХ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'фармат_b87fd068', 'main': 'Выканаць', 'content': 'кантэнт_значэнне', 'source': '원본자료', 'name': 'Назва', 'reference': 'Параўнанне_базавы_план', 'ROOT': '기준', 'value': 'значэнне', 'report': 'праверка_справаздача'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
