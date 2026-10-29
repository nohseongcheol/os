#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/працоўны_стол_выгляд.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('працоўны_стол_выгляд', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('працоўны_стол_выгляд')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ПАМЫЛКА', 'exact': '정확한값', 'network': 'Сетка', 'closed': '닫힘', 'length': 'даўжыня_значэнне', 'opened': '열림', 'ftp_port': 'файл_перанос_нумар_порта', 'server': 'сервер_значэнне', 'resources': 'Рэсурсы', 'data': 'дадзеныя', 'shift': 'клавіша_SHIFT', 'send': 'адправіць', 'run_desktop': 'паток_працоўны_стол', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'вузел', 'text': 'Тэкст', 'korean': '한글여부', 'port': 'нумар_порта', 'signum': '신호번호', 'version': '판번호', 'parser': 'аналізатар', 'bridge': 'мост', 'kind': 'катэгорыя_значэнне', 'tail': '끝부분', 'size': 'Памер', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'кліент', 'char': 'сімвал_дадзеныя_4d9f8719', 'work': '작업경로', 'Keyboard': 'клавіятура', 'x': 'каардыната_x', 'down': '누르는중', 'net': 'Сетка_мост_увядзенне', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_масіў', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Працэс', 'Desktop': 'злучаць_працоўны_стол', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'пераход_рэжым', 'command': 'Загад', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'кіраванне_клавіша', 'path': 'ШЛЯХ', 'cp': 'сімвал_кадаванне', 'terminate': '종료시키기', 'security': 'Бяспека', 'vnc_port': '원격화면접속번호', 'body': 'асноўны_тэкст', 'index': '색인', 'exited': '종료됨', 'keysym': 'клавіша_сімвал', 'output': '출력결과', 'keyboard': 'клавіятура_увядзенне', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'чытач', 'NetworkBridge': 'Сетка_мост', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
