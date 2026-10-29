#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/выканаць_файл.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('выканаць_файл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('выканаць_файл')
    대응 = {'timeout': '시간제한', 's': 'радок_дадзеныя', 'i': '순번', 'match': '일치', 'files': 'файл_Спіс', 'program': 'праграма', 'executable': '실행가능파일', 'args': 'аргумент_масіў', 'chunk': '조각', 'data': 'дадзеныя', 'proc': 'Працэс', 'send': 'адправіць', 'main': 'Выканаць', 'marker': '확인표시', 'command': 'Загад', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'выканаць_каманда', 'p': '자료위치', 'parser': 'аналізатар', 'options': 'Параметры', 'kind': 'катэгорыя_значэнне', 'selector': 'селектар', 'upload_data': 'запампоўка_дадзеныя', 'end': 'скончыць_Зрух', 'n': '개수', 'd': 'прызначэнне_дадзеныя', 'key': '누름값', 'output': '출력결과', 'line': 'лінія', 'name': 'Назва', 'upload_name': 'запампоўка_імя', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
