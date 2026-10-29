#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/파일전송시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'қобилият_иттилоот', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'иттилоот', 'proc': 'Раванд', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Бойгонӣ', 'main': 'порча', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'собит_манбаъ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Матн', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'фармон', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'сервер_манбаъ', 'shell': 'восит', 'upload': 'бор_кардан_Файлҳо', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'кӯпрук', 'selector': 'интихобкунанда', 'end': 'анҷом_додан_Интиқолшавӣ', 'e': '보조항목', 'ftp': 'файл_интиқол_пайваст', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ҳамсон_қимат', 'result': '결과', 'unchanged': '보존자료', 'line': 'хат', 'server_tcp_port': 'сервер_ҷараён_порт', 'source': '원본자료', 'NetworkBridge': 'Шабака_кӯпрук', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'санҷиши_эътибор_гузориш'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
