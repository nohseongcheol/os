#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/예제시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'файл_перанос_нумар_порта', 'data': 'дадзеныя', 'graphics_command': '그림명령', 'main': 'Выканаць', 'row': '행위치', 'init': '초기값', 'target': 'мэтавы_паказчык', 'ROOT': '기준', 'text': 'Тэкст', 'binary': 'дваічны', 'out': '결과자료', 'entry': 'увядзенне_бал', 'got': '받은수', 'port': 'нумар_порта', 'graphics_start': 'Пуск_рукапісная_графіка', 'col': '열위치', 'begin': 'Пуск_Зрух', 'kind': 'катэгорыя_значэнне', 'selector': 'селектар', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'кліент', 'line': 'лінія', 'report': 'праверка_справаздача', 'language': 'Мова', 'x': 'каардыната_x', 'start': 'Выканаць', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'адправіць_Спіс', 'payload': 'карыснае_змесціва_дадзеныя', 'proc': 'Працэс', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'імя_табліца', 'content': 'кантэнт_значэнне', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'файл_увядзенне_імя', 'shell': 'абалонка', 'color': '색상', 'transcript': '대화기록', 'offset': 'Зрух_значэнне', 'h': '높이값', 'run': 'выканаць_каманда', 'c': 'код_сімвала', 'path': 'ШЛЯХ', 'encoding': 'набор_сімвалаў', 'end': 'скончыць_Зрух', 'ftp': 'файл_перанос_кантакт', 'pixels': '화소들', 'symbol': 'сімвал_значэнне', 'source': '원본자료', 'name': 'Назва', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
