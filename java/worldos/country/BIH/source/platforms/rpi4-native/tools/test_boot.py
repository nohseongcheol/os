#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Мрежа_порука', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': '실행하기', 'cancel': 'отказати_операција', 'cmd_byte': 'команда_бајт', 'reply': '응답', 'points': '지점들', 'server': 'сервер_вриједност', 'data': 'подаци', 'prompt': 'промпт', 'enter': 'унијети', 'imported': '들여온파일', 'send': 'послати', 'main': '시작', 'ROOT': '기준', 'text': 'текст', 'first_gui': '첫화면', 'pixel': 'Пел', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'Пел_фајл', 'pixels_data': 'Пел_подаци', 'edit': 'уређивати_вриједност', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'подесити_величину', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'клијент', 'line': 'редак', 'report': 'провјера_извјештај', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'преузети', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'процес', 'content': 'Садржај_вриједност', 'block': 'подаци_блокирати', 'marker': '확인표시', 'command': 'команда', 'expected': '예상결과', 'shell': 'љуска', 'drawing': 'уцртавање_пут', 'f': 'фајл_унос', 'transcript': '대화기록', 'offset': '변위', 'path': 'пут', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ток_вриједност', 'cmd': '명령인수', 'name': 'назив', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
