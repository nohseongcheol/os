#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/파일전송시험.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('파일전송시험')
    зіставлення_значення = {'timeout': '시간제한', 'payload': 'вміст_пакета_дані', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'дані', 'proc': 'Процеси', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Архів', 'main': 'запустити', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'відлуння_сервер_запис', 'ROOT': 'Дії_корінь', 'text': 'текст', 'marker': 'маркер', 'EchoFixture': '되돌림시험서버', 'command': 'команда', 'out': 'КР_дані', 'expected': '예상결과', 'server_source': 'сервер_джерело', 'shell': 'оболонка', 'upload': 'передавати_Файли', 'transcript': 'транскрипт', 'port': 'номер_порту', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'сервер_дейтаграма_порт', 'packed': '묶인자료', 'bridge': 'міст', 'selector': 'селектор', 'end': 'завершити_виклик_Зміщена_копія', 'e': '보조항목', 'ftp': 'передавання_файлу_зв_язок', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'точка_значення', 'result': 'результат', 'unchanged': '보존자료', 'line': 'рядок_введення', 'server_tcp_port': 'сервер_потік_порт', 'source': '원본자료', 'NetworkBridge': 'міст_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'отримувати_повідомлення', 'report': 'перевірка_звіт'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
