#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/파일전송시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'დატვირთვა_მონაცემები', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'მონაცემები', 'proc': 'პროცესი', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'არქივი', 'main': 'გაშვება', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'სტატიკური_წყარო', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ბრძანება', 'out': 'გაზომვა_მონაცემები', 'expected': '예상결과', 'server_source': 'სერვერი_წყარო', 'shell': 'გარემო', 'upload': 'ატვირთვა_ფაილები', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ხიდი', 'selector': 'სელექტორი', 'end': 'დასასრული_ოფსეტი', 'e': '보조항목', 'ftp': 'ფაილი_გადატანა_კავშირი', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'კვანძი_მნიშვნელობა_6a3b6fa7', 'result': 'გაზომვა', 'unchanged': '보존자료', 'line': 'ხაზი', 'server_tcp_port': 'სერვერი_ნაკადი_პორტი', 'source': '원본자료', 'NetworkBridge': 'ქსელი_ხიდი', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'გადამოწმება_ანგარიში'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
