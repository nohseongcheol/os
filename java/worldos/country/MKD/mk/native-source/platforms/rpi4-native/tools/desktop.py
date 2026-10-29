#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/десктоп_Приказ.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('десктоп_Приказ', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('десктоп_Приказ')
    대응 = {'count': 'внес_COUNT', 'special': '특수글쇠', 'error': 'ГРЕШКА', 'exact': 'EXACT_VALUE', 'network': 'Мрежа', 'closed': '닫힘', 'length': 'должина_VALUE', 'opened': '열림', 'ftp_port': 'датотека_пренос_број_на_порта', 'server': 'сервер_VALUE', 'resources': 'Ресурси', 'data': 'податоци', 'shift': 'копче_SHIFT', 'send': 'испрати', 'run_desktop': 'изврши_десктоп', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'вдоми', 'text': 'Текст', 'korean': '한글여부', 'port': 'број_на_порта', 'signum': '신호번호', 'version': 'број_на_верзија', 'parser': 'анализатор', 'bridge': 'мост', 'kind': 'област_VALUE', 'tail': '끝부분', 'size': 'Големина', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клиент', 'char': 'знак_податоци', 'work': '작업경로', 'Keyboard': 'тастатура', 'x': 'координата_х', 'down': '누르는중', 'net': 'Мрежа_мост_внес', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_низа', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процес', 'Desktop': 'ПОВРЗИ_десктоп', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'ПАТЕКА', 'cp': 'знак_кодирање', 'terminate': '종료시키기', 'security': 'Безбедност', 'vnc_port': '원격화면접속번호', 'body': 'основен_текст', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Клуч_симбол', 'output': '출력결과', 'keyboard': 'тастатура_внес', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Читач', 'NetworkBridge': 'Мрежа_мост', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
