#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/원격한글시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Орындау_2', 'profile': 'Профиль', 'focused': 'Cұрыпталған', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_мән', 'log': 'журнал_жол', 'args': 'аргумент_массив', 'deadline': 'ең_соңғы_мерзім_уақыт', 'data': 'деректер', 'candidate': '후보', 'logs': '기록들', 'kw': 'деректі_аргумент', 'number': '수치', 'main': 'Орындау_2', 'ready': '준비완료', 'found': 'Іздеу_өлшем', 'guest': 'қонақ', 'ROOT': 'жоба_түбір', 'marker': '확인표시', 'text': 'Мәтін', 'out': 'өлшем_деректер', 'env': '환경', 'f': 'файл_енгізу', 'port': 'порт_нөмірі', 'offset': 'жылжыту_мән_450fc799', 'version': 'Нұсқа_нөмірі', 'p': 'деректер_лауазым', 'selector': 'селектор', 'xvfb': 'виртуалды_дисплей', 'display': 'дисплей', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Аты', 'window': 'Терезе', 'report': 'тексерім_есеп', 'work': '작업경로'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
