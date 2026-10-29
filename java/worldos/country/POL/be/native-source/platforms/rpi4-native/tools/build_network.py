#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/зборка_Сетка.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('зборка_Сетка', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('зборка_Сетка')
    대응 = {'obj': 'канчатковы_файл', 'objects': 'прызначэнне_Файлы', 'library': 'бібліятэка', 'output': '출력결과', 'port': 'нумар_порта', 'root': '뿌리주소', 'files': 'файл_Спіс', 'source': '원본자료', 'run': 'выканаць_каманда', 'flags': 'канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў', 'path': 'ШЛЯХ', 'build_network': 'стварыць_Сетка', 'cc': '시언어번역기', 'ar': 'Архіў_інструмент'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
