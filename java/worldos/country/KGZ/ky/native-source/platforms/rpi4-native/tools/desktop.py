#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/иш_такта_көрүү.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('иш_такта_көрүү', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('иш_такта_көрүү')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Ката', 'exact': '정확한값', 'network': 'Желе', 'closed': '닫힘', 'length': 'узундук_маани', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'сервер_маани', 'resources': 'Ресурстар', 'data': 'берилмелер', 'shift': 'SHIFT_баскычы', 'send': 'жөнөтүү', 'run_desktop': 'топтом_иш_такта', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'кабылдоо', 'text': 'Текст', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'категория_маани', 'tail': '끝부분', 'size': 'Өлчөмү', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'керектөөчү', 'char': 'символ_берилмелер_4d9f8719', 'work': '작업경로', 'Keyboard': 'баскычтоп', 'x': 'x_координата', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_МАССИВ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процесси', 'Desktop': 'ТУТАШУУ_иш_такта', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'котормо_режим', 'command': 'Команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_баскычы', 'path': 'ЖОЛ', 'cp': 'символ_коддоо', 'terminate': '종료시키기', 'security': 'Коопсуздук', 'vnc_port': '원격화면접속번호', 'body': 'негизги_текст', 'index': '색인', 'exited': '종료됨', 'keysym': 'ачкыч_символ', 'output': '출력결과', 'keyboard': 'баскычтоп_киргизме_жазуу', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'окуучу', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
