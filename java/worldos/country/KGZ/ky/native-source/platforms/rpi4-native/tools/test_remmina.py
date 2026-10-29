#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/원격한글시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Жүргүзүү', 'profile': 'Профиль', 'focused': 'Маанилүү', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_маани', 'log': 'жазуу_катар', 'args': 'аргумент_МАССИВ', 'deadline': '마감시각', 'data': 'берилмелер', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Жүргүзүү', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Текст', 'out': '결과자료', 'env': '환경', 'f': 'файл_киргизме_жазуу', 'port': '접속번호', 'offset': 'Жылбышуу_маани', 'version': '판번호', 'p': '자료위치', 'selector': 'селектор', 'xvfb': 'виртуалдык_дисплей', 'display': 'дисплей', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Аты', 'window': 'терезе', 'report': 'ырастоо_отчет', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
