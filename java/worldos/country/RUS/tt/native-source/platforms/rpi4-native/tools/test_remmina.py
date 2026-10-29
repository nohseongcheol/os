#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'эшләтү', 'profile': 'Профиль', 'focused': 'Тупланылган', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_VALUE', 'log': 'LOG_юл', 'args': 'аргумент_МАССИВ', 'deadline': '마감시각', 'data': 'мәгълүмат', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'эшләтү', 'ready': '준비완료', 'found': 'Эзләү_үлчәм', 'guest': 'кунак', 'ROOT': 'экранга_җибәрү_тамыр', 'marker': '확인표시', 'text': 'Mäten', 'out': 'үлчәм_мәгълүмат', 'env': '환경', 'f': 'файл_кертү', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'мәгълүмат_урнаштыру', 'selector': 'сайлагыч', 'xvfb': 'виртуаль_дисплей', 'display': 'дисплей', 'n': 'элемент_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'исем', 'window': 'тәрәз', 'report': 'раслау_отчет', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
