#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/классик_карау.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('классик_карау', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('классик_карау')
    대응 = {'count': 'кертү_COUNT', 'special': '특수글쇠', 'error': 'Хата', 'exact': 'EXACT_VALUE', 'network': 'Челтәр', 'closed': '닫힘', 'length': 'озынлык_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'сервер_VALUE', 'resources': 'Ресурслар', 'data': 'мәгълүмат', 'shift': 'SHIFT_төймәсе', 'send': 'җибәрү', 'run_desktop': 'эшләтү_классик', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост', 'text': 'Mäten', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'күпер', 'kind': 'категория_VALUE', 'tail': '끝부분', 'size': 'үлчәмен_үзгәртү', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клиент', 'char': 'символ_мәгълүмат_4d9f8719', 'work': '작업경로', 'Keyboard': 'төймәсар', 'x': 'X_координатасы', 'down': '누르는중', 'net': 'Челтәр_күпер_кертү', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_МАССИВ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процесс', 'Desktop': 'ялгау_классик', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Yul', 'cp': 'символ_кодлау', 'terminate': '종료시키기', 'security': 'Иминлек', 'vnc_port': '원격화면접속번호', 'body': 'төп_текст', 'index': 'Эзләү_INDEX', 'exited': '종료됨', 'keysym': 'ачкыч_символ', 'output': '출력결과', 'keyboard': 'төймәсар_кертү', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'укучы', 'NetworkBridge': 'Челтәр_күпер', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
