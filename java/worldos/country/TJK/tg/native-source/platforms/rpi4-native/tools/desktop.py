#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/мизи_корӣ_намуд.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('мизи_корӣ_намуд', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('мизи_корӣ_намуд')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Хато', 'exact': '정확한값', 'network': 'Шабака', 'closed': '닫힘', 'length': 'дарозӣ_қимат', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'сервер_қимат', 'resources': 'Захираҳо', 'data': 'иттилоот', 'shift': 'тугмаи_SHIFT', 'send': 'фиристодан', 'run_desktop': 'порча_мизи_корӣ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'мизбон', 'text': 'Матн', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'кӯпрук', 'kind': 'категория_қимат', 'tail': '끝부분', 'size': 'андоза_кардан', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'муштарӣ', 'char': 'аломат_иттилоот_4d9f8719', 'work': '작업경로', 'Keyboard': 'клавиатура', 'x': 'координатаи_х', 'down': '누르는중', 'net': 'Шабака_кӯпрук_ворида', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_қатор', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Раванд', 'Desktop': 'ПАЙВАСТ_мизи_корӣ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'қатъу_васл_кардан_ҳолат', 'command': 'фармон', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'идоракунӣ_калид', 'path': 'масир', 'cp': 'аломат_рамзгузорӣ', 'terminate': '종료시키기', 'security': 'Амният', 'vnc_port': '원격화면접속번호', 'body': 'матни_асосӣ', 'index': '색인', 'exited': '종료됨', 'keysym': 'калид_аломат', 'output': '출력결과', 'keyboard': 'клавиатура_ворида', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Хонанда', 'NetworkBridge': 'Шабака_кӯпрук', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
