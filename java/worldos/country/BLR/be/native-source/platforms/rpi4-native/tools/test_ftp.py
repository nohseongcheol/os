#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/파일전송시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'карыснае_змесціва_дадзеныя', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'дадзеныя', 'proc': 'Працэс', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Архіў', 'main': 'Выканаць', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'статычны_крыніца', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Тэкст', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Загад', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'сервер_крыніца', 'shell': 'абалонка', 'upload': 'запампоўка_Файлы', 'transcript': '대화기록', 'port': 'нумар_порта', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'мост', 'selector': 'селектар', 'end': 'скончыць_Зрух', 'e': '보조항목', 'ftp': 'файл_перанос_кантакт', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'аднарангавы_значэнне', 'result': '결과', 'unchanged': '보존자료', 'line': 'лінія', 'server_tcp_port': 'сервер_паток_порт', 'source': '원본자료', 'NetworkBridge': 'Сетка_мост', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'праверка_справаздача'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
