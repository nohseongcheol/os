#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/파일전송시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': '내용자료', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': '자료', 'proc': '실행과정', 'code': '명령열', 'linux': '리눅스파일', 'archive': '압축꾸러미', 'main': 'Tandika', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Bigambo', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Mulimu', 'out': '결과자료', 'expected': '예상결과', 'server_source': '서버원문', 'shell': '셸', 'upload': '올리기', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': '준비선택기', 'end': '끝위치', 'e': '보조항목', 'ftp': '파일전송접속', 'key': '누름값', 'bytecode': '바이트코드', 'peer': '상대', 'result': 'KIGENDERWA', 'unchanged': '보존자료', 'line': '줄', 'server_tcp_port': '서버연결접속번호', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': '검증기록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
