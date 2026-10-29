#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/원격한글시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'порча', 'profile': 'Профил', 'focused': 'Мураттаб', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_қимат', 'log': 'сабт_кардан_сабт', 'args': 'аргумент_қатор', 'deadline': '마감시각', 'data': 'иттилоот', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'порча', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'меҳмон', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Матн', 'out': '결과자료', 'env': '환경', 'f': 'файл_ворида', 'port': '접속번호', 'offset': 'Интиқолшавӣ_қимат', 'version': '판번호', 'p': '자료위치', 'selector': 'интихобкунанда', 'xvfb': 'виртуалӣ_дисплей', 'display': 'дисплей', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ном', 'window': 'равзана', 'report': 'санҷиши_эътибор_гузориш', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
