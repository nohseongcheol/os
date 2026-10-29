#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/파일전송시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'корисни_подаци_подаци', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'подаци', 'proc': 'Процес', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Архива', 'main': 'Покрени', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'статични_извор', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'пројектовати_корен', 'text': 'Текст', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Наредба', 'out': 'мера_подаци', 'expected': '예상결과', 'server_source': 'сервер_извор', 'shell': 'љуска', 'upload': 'Отпрема_Фајлови', 'transcript': 'транскрипт', 'port': 'број_порта', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'мост', 'selector': 'бирач', 'end': 'завршити_Помак', 'e': '보조항목', 'ftp': 'фајл_пренос_веза', 'key': '누름값', 'bytecode': '바이트코드', 'peer': '상대', 'result': 'ИСХОД', 'unchanged': '보존자료', 'line': 'Ред', 'server_tcp_port': 'сервер_ток_порт', 'source': '원본자료', 'NetworkBridge': 'Мрежа_мост', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'провјера_извештај'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
