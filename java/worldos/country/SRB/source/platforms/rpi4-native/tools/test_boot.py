#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/부팅시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'одговор_1262b476', 'msg': 'Мрежа_порука', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Изврши', 'cancel': 'Откажи_операција', 'cmd_byte': 'команда_бајт', 'reply': 'одговор', 'points': '지점들', 'server': 'сервер_вриједност', 'data': 'подаци', 'prompt': 'одзив', 'enter': 'унети', 'imported': '들여온파일', 'send': 'послати', 'main': 'Покрени', 'ROOT': 'пројектовати_корен', 'text': 'Текст', 'first_gui': '첫화면', 'pixel': 'пиксел', 'java_class': '자바클래스', 'upload': 'Отпрема_Фајлови', 'pixels_file': 'пиксел_фајл', 'pixels_data': 'пиксел_подаци', 'edit': 'Уреди_вриједност', 'receive_until': '표시까지받기', 'selector': 'бирач', 'size': 'Величина', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'дугме_Y_координата', 'result': 'ИСХОД', 'samples': '예제들', 'client': 'клијент', 'line': 'Ред', 'report': 'провјера_извештај', 'work': '작업경로', 'x': 'x_координата', 'python_checks': '파이썬검사', 'download': 'преузми', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Процес', 'content': 'Садржај_вриједност', 'block': 'подаци_блокирај', 'marker': '확인표시', 'command': 'Наредба', 'expected': '예상결과', 'shell': 'љуска', 'drawing': 'цртеж_пут', 'f': 'фајл_унос', 'transcript': 'транскрипт', 'offset': 'Помак_вриједност', 'path': 'ПУТАЊА', 'screenshot': 'исечак_екрана', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ток_вриједност', 'cmd': '명령인수', 'name': 'Назив', 'qmp': '모의제어접속'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
