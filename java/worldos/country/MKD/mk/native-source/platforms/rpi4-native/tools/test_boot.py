#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Мрежа_порака', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Изврши', 'cancel': 'Откажи_операција', 'cmd_byte': 'наредба_бајт', 'reply': 'одговори', 'points': '지점들', 'server': 'сервер_VALUE', 'data': 'податоци', 'prompt': 'промпт', 'enter': 'внеси', 'imported': '들여온파일', 'send': 'испрати', 'main': 'Изврши_2', 'ROOT': 'Project_корен', 'text': 'Текст', 'first_gui': '첫화면', 'pixel': 'пиксел', 'java_class': '자바클래스', 'upload': 'постави_Датотеки', 'pixels_file': 'пиксел_датотека', 'pixels_data': 'пиксел_податоци', 'edit': 'уреди_VALUE', 'receive_until': '표시까지받기', 'selector': 'избирач', 'size': 'Големина', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_ГУИ', 'y': '세로좌표', 'result': 'мерка', 'samples': '예제들', 'client': 'клиент', 'line': 'ред', 'report': 'проверка_извештај', 'work': '작업경로', 'x': 'координата_х', 'python_checks': '파이썬검사', 'download': 'преземи', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Процес', 'content': 'Содржина_VALUE', 'block': 'податоци_блокирај', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'shell': 'обвивка', 'drawing': 'цртеж_патека', 'f': 'датотека_внес', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'ПАТЕКА', 'screenshot': 'Отсекување_екран', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Име', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
