#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/파일전송시험.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    съпоставяне_стойност = {'timeout': '시간제한', 'payload': 'полезен_обем_данни', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'данни', 'proc': 'Процес', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Архив', 'main': 'Стартиране', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'Ехо_сървър_запис', 'ROOT': 'проект_корен', 'text': 'Текст', 'marker': 'маркер', 'EchoFixture': '되돌림시험서버', 'command': 'Команда', 'out': 'мярка_данни', 'expected': '예상결과', 'server_source': 'сървър_източник', 'shell': 'обвивка', 'upload': 'качвам_Файлове', 'transcript': 'препис', 'port': 'номер_на_порт', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'сървър_дейтаграма_порт', 'packed': '묶인자료', 'bridge': 'мост', 'selector': 'свързан_елемент_за_избор', 'end': 'прекратяване_на_повикването_Изместване', 'e': '보조항목', 'ftp': 'прехвърляне_на_файл_връзка', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'крайно_устройство_стойност', 'result': 'РЕЗУЛТАТ', 'unchanged': '보존자료', 'line': 'ред', 'server_tcp_port': 'сървър_поток_порт', 'source': '원본자료', 'NetworkBridge': 'мост_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'получавам_имейл', 'report': 'проверка_отчет'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
