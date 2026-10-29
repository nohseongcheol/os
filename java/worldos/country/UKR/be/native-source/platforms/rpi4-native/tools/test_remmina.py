#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/원격한글시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Выканаць', 'profile': 'Профіль', 'focused': 'Важнае', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_значэнне', 'log': 'журнал_запіс', 'args': 'аргумент_масіў', 'deadline': '마감시각', 'data': 'дадзеныя', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Выканаць', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'госць', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Тэкст', 'out': '결과자료', 'env': '환경', 'f': 'файл_увядзенне', 'port': 'нумар_порта', 'offset': 'Зрух_значэнне', 'version': '판번호', 'p': '자료위치', 'selector': 'селектар', 'xvfb': 'віртуальны_дысплэй', 'display': 'дысплэй', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Назва', 'window': 'акно', 'report': 'праверка_справаздача', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
