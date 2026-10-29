#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/원격한글시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Покрени', 'profile': 'Профил', 'focused': 'У_фокусу', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_вриједност', 'log': 'евиденција_ред', 'args': 'аргумент_низ', 'deadline': '마감시각', 'data': 'подаци', 'candidate': '후보', 'logs': '기록들', 'kw': 'именовани_аргумент', 'number': '수치', 'main': 'Покрени', 'ready': '준비완료', 'found': 'тражити_мера', 'guest': 'гост', 'ROOT': 'пројектовати_корен', 'marker': '확인표시', 'text': 'Текст', 'out': 'мера_подаци', 'env': 'радно_окружење', 'f': 'фајл_унос', 'port': 'број_порта', 'offset': 'Помак_вриједност', 'version': '판번호', 'p': 'подаци_позиција', 'selector': 'бирач', 'xvfb': 'виртуелно_екран', 'display': 'екран', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Назив', 'window': 'Прозор', 'report': 'провјера_извештај', 'work': '작업경로'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
