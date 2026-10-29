#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/десктоп_Приказ.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('десктоп_Приказ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('десктоп_Приказ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ГРЕШКА', 'exact': '정확한값', 'network': 'Мрежа', 'closed': '닫힘', 'length': 'дужина_вриједност', 'opened': '열림', 'ftp_port': 'фајл_пренос_број_порта', 'server': 'сервер_вриједност', 'resources': 'Извори', 'data': 'подаци', 'shift': 'тастер_SHIFT', 'send': 'послати', 'run_desktop': 'низ_десктоп', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост', 'text': 'Текст', 'korean': '한글여부', 'port': 'број_порта', 'signum': '신호번호', 'version': '판번호', 'parser': 'анализатор', 'bridge': 'мост', 'kind': 'област_вриједност', 'tail': '끝부분', 'size': 'Величина', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'дугме_Y_координата', 'prefix': '앞부분', 'client': 'клијент', 'char': 'знак_подаци', 'work': '작업경로', 'Keyboard': 'тастатура', 'x': 'x_координата', 'down': '누르는중', 'net': 'Мрежа_мост_унос', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_низ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процес', 'Desktop': 'ПОВЕЖИ_десктоп', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'пребацити_мод', 'command': 'Наредба', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'тастер_CTRL', 'path': 'ПУТАЊА', 'cp': 'знак_кодирање', 'terminate': '종료시키기', 'security': 'Безбедност', 'vnc_port': '원격화면접속번호', 'body': 'тело_текста', 'index': 'Претрага_индекс', 'exited': '종료됨', 'keysym': 'Кључ_симбол', 'output': '출력결과', 'keyboard': 'тастатура_унос', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Читач', 'NetworkBridge': 'Мрежа_мост', 'gui': '그림화면', 'worker': 'обрада_задатак'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
