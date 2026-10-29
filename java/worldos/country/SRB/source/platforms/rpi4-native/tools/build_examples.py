#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/예제빌드.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'мера_подаци', 'build_examples': '예제만들기', 'files': 'фајл_Листа', 'java': '자바실행', 'run': 'Изврши_команда', 'path': 'ПУТАЊА', 'p': 'подаци_позиција', 'readme': 'Прочитај_ме', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Претрага_индекс', 'classes': 'класа_пут', 'repo': 'депо_пут', 'root': 'корен_адреса', 'content': 'Садржај_вриједност', 'source': '원본자료', 'name': 'Назив', 'target': 'циљ', 'manifest': '꾸러미명세', 'language': 'Језик'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
