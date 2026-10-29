#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'капацитет_податоци', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'податоци', 'proc': 'Процес', 'code': 'инструкција_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Архива', 'main': 'Изврши_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'статичен_извор', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_корен', 'text': 'Текст', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Команда', 'out': 'мерка_податоци', 'expected': '예상결과', 'server_source': 'сервер_извор', 'shell': 'обвивка', 'upload': 'постави_Датотеки', 'transcript': '대화기록', 'port': 'број_на_порта', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'мост', 'selector': 'избирач', 'end': 'крај_OFFSET', 'e': '보조항목', 'ftp': 'датотека_пренос_врска', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'рамноправен_уред_VALUE', 'result': 'мерка', 'unchanged': '보존자료', 'line': 'ред', 'server_tcp_port': 'сервер_Stream_порта', 'source': '원본자료', 'NetworkBridge': 'Мрежа_мост', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'проверка_извештај'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
