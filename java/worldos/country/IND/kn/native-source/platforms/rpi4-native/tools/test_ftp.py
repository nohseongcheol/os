#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/파일전송시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ಪೇಲೋಡ್_ಡೇಟಾ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ಡೇಟಾ', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ಅರ್ಖೀವ್', 'main': 'ಚಲಾಯಿಸು_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ಸ್ಥಾಯಿ_ಮೂಲ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ಆಜ್ಞೆ', 'out': 'ಮಾಪನ_ಡೇಟಾ', 'expected': '예상결과', 'server_source': 'ಸರ್ವರ್_ಮೂಲ', 'shell': 'ಶೆಲ್', 'upload': 'ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು', 'transcript': '대화기록', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ಸೇತುವೆ', 'selector': 'ಸೆಲೆಕ್ಟರ್', 'end': 'ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್', 'e': '보조항목', 'ftp': 'ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ಪೀರ್_ಮೌಲ್ಯ', 'result': 'ಮಾಪನ', 'unchanged': '보존자료', 'line': 'ಸಾಲು', 'server_tcp_port': 'ಸರ್ವರ್_ಸ್ಟ್ರೀಮ್_ಪೋರ್ಟ್', 'source': '원본자료', 'NetworkBridge': 'ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ದೃಢೀಕರಣ_ವರದಿ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
