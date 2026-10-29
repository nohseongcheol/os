#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Челтәр_хәбәр', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Башкару', 'cancel': 'баш_тарту_гамәл', 'cmd_byte': 'команда_байт', 'reply': 'җавап_бирү', 'points': '지점들', 'server': 'сервер_VALUE', 'data': 'мәгълүмат', 'prompt': 'тәкъдим', 'enter': 'кертү', 'imported': '들여온파일', 'send': 'җибәрү', 'main': 'эшләтү', 'ROOT': 'экранга_җибәрү_тамыр', 'text': 'Mäten', 'first_gui': '첫화면', 'pixel': 'нокта', 'java_class': '자바클래스', 'upload': 'йөкләп_җибәрү_Файллар', 'pixels_file': 'нокта_файл', 'pixels_data': 'нокта_мәгълүмат', 'edit': 'төзәтү_VALUE', 'receive_until': '표시까지받기', 'selector': 'сайлагыч', 'size': 'үлчәмен_үзгәртү', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'үлчәм', 'samples': '예제들', 'client': 'клиент', 'line': 'юл', 'report': 'раслау_отчет', 'work': '작업경로', 'x': 'X_координатасы', 'python_checks': '파이썬검사', 'download': 'йөкләү_496ddb99', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Процесс', 'content': 'Эчтәлек_VALUE', 'block': 'мәгълүмат_тыю', 'marker': '확인표시', 'command': 'команда', 'expected': '예상결과', 'shell': 'тышча', 'drawing': 'сызым_юл', 'f': 'файл_кертү', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'Yul', 'screenshot': 'Экран_кисемтәсе', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'агым_VALUE', 'cmd': '명령인수', 'name': 'исем', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
