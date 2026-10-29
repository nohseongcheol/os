#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/радна_површина_поглед.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('радна_површина_поглед', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('радна_површина_поглед')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'грешка', 'exact': '정확한값', 'network': 'Мрежа', 'closed': '닫힘', 'length': 'дужина_вриједност', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'сервер_вриједност', 'resources': 'Ресурси', 'data': 'подаци', 'shift': 'типка_SHIFT', 'send': 'послати', 'run_desktop': '바탕화면실행', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост_рачунар', 'text': 'текст', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'категорија_вриједност', 'tail': '끝부분', 'size': 'подесити_величину', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клијент', 'char': 'знак_подаци', 'work': '작업경로', 'Keyboard': 'тастатура', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_низ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'процес', 'Desktop': 'повезати_радна_површина', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'промијенити_мод', 'command': 'команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'пут', 'cp': 'знак_кодирање', 'terminate': '종료시키기', 'security': 'сигурност', 'vnc_port': '원격화면접속번호', 'body': 'Тијело_текста', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': 'тастатура_унос', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'читач', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
