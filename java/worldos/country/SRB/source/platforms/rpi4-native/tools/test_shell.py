#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/셸시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_координата', 'msg': 'Мрежа_порука', 'i': '순번', 'reply': 'одговор', 'call': '호출', 'args': 'аргумент_низ', 'chunk': '조각', 'data': 'подаци', 'proc': 'Процес', 'long_text': '긴글', 'restored': '복원자료', 'send': 'послати', 'file': 'Датотека', 'main': 'Покрени', 'found': 'тражити_мера', 'ROOT': 'пројектовати_корен', 'text': 'Текст', 'marker': '확인표시', 'command': 'Наредба', 'expected': '예상결과', 'pixel': 'пиксел', 'shell': 'љуска', 'poll': '준비살피미', 'transcript': 'транскрипт', 'end': 'завршити_Помак', 'image': 'слика', 'key': '누름값', 'y': 'дугме_Y_координата', 'output': '출력결과', 'result': 'ИСХОД', 'client': 'клијент', 'line': 'Ред', 'stream': 'ток_вриједност', 'name': 'Назив', 'value': 'вриједност', 'receive': '수신하기', 'report': 'провјера_извештај', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
