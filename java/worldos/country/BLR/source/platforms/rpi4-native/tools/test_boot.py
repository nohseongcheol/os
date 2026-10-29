#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/부팅시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Сетка_ліст', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Выкананне', 'cancel': 'Адмена_аперацыя', 'cmd_byte': 'каманда_байт', 'reply': 'адказаць', 'points': '지점들', 'server': 'сервер_значэнне', 'data': 'дадзеныя', 'prompt': 'запыт', 'enter': 'увесці', 'imported': '들여온파일', 'send': 'адправіць', 'main': 'Выканаць', 'ROOT': '기준', 'text': 'Тэкст', 'first_gui': '첫화면', 'pixel': 'пэл', 'java_class': '자바클래스', 'upload': 'запампоўка_Файлы', 'pixels_file': 'пэл_файл', 'pixels_data': 'пэл_дадзеныя', 'edit': 'рэдагаваць_значэнне', 'receive_until': '표시까지받기', 'selector': 'селектар', 'size': 'Памер', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'кліент', 'line': 'лінія', 'report': 'праверка_справаздача', 'work': '작업경로', 'x': 'каардыната_x', 'python_checks': '파이썬검사', 'download': 'спампоўка', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Працэс', 'content': 'кантэнт_значэнне', 'block': 'дадзеныя_блакіраваць', 'marker': '확인표시', 'command': 'Загад', 'expected': '예상결과', 'shell': 'абалонка', 'drawing': 'рукапісная_графіка_шлях', 'f': 'файл_увядзенне', 'transcript': '대화기록', 'offset': 'Зрух_значэнне', 'path': 'ШЛЯХ', 'screenshot': 'здымак_экрана', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'паток_значэнне', 'cmd': '명령인수', 'name': 'Назва', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
