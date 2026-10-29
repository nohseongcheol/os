#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/үстелдік_Көрініс.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('үстелдік_Көрініс', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('үстелдік_Көрініс')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Қате', 'exact': '정확한값', 'network': 'желі', 'closed': '닫힘', 'length': 'ұзындық_мән', 'opened': '열림', 'ftp_port': 'файл_тасымалдау_порт_нөмірі', 'server': 'сервер_мән', 'resources': 'Ресурстар', 'data': 'деректер', 'shift': 'SHIFT_пернесі', 'send': 'жіберу', 'run_desktop': 'орындалу_үстелдік', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'орналастыру', 'text': 'Мәтін', 'korean': '한글여부', 'port': 'порт_нөмірі', 'signum': '신호번호', 'version': 'Нұсқа_нөмірі', 'parser': 'талдау_құралы', 'bridge': 'көпір', 'kind': 'Санат_мән', 'tail': '끝부분', 'size': 'Өлшемі', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_түймешігі_координата', 'prefix': '앞부분', 'client': 'клиент', 'char': 'символдық_деректер', 'work': '작업경로', 'Keyboard': 'пернетақта', 'x': 'x_координатасы', 'down': '누르는중', 'net': 'желі_көпір_енгізу', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_массив', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Үрдіс', 'Desktop': 'қосу_үстелдік', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ауысу_режим', 'command': 'Команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_пернесі', 'path': 'Жол_2', 'cp': 'символдарды_кодтау', 'terminate': '종료시키기', 'security': 'Қауіпсіздік', 'vnc_port': '원격화면접속번호', 'body': 'негізгі_мәтін', 'index': 'Іздеу_индекс', 'exited': '종료됨', 'keysym': 'Кілт_символ', 'output': '출력결과', 'keyboard': 'пернетақта_енгізу', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'оқушы', 'NetworkBridge': 'желі_көпір', 'gui': '그림화면', 'worker': 'өңдеу_тапсырма'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
