#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/부팅시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ಚಲಾಯಿಸು', 'cancel': 'ರದ್ದು_ಆಪರೇಶನ್', 'cmd_byte': 'ಆದೇಶ_ಬೈಟ್', 'reply': 'ಪ್ರತ್ಯುತ್ತರ', 'points': '지점들', 'server': 'ಸರ್ವರ್_ಮೌಲ್ಯ', 'data': 'ಡೇಟಾ', 'prompt': 'ಪ್ರಾಂಪ್ಟ್', 'enter': 'ನಮೂದಿಸು', 'imported': '들여온파일', 'send': 'ಕಳುಹಿಸಿ', 'main': 'ಚಲಾಯಿಸು_2', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'first_gui': '첫화면', 'pixel': 'ಪೆಲ್', 'java_class': '자바클래스', 'upload': 'ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು', 'pixels_file': 'ಪೆಲ್_ಫೈಲ್', 'pixels_data': 'ಪೆಲ್_ಡೇಟಾ', 'edit': 'ಸಂಪಾದನೆ_ಮೌಲ್ಯ', 'receive_until': '표시까지받기', 'selector': 'ಸೆಲೆಕ್ಟರ್', 'size': 'ಗಾತ್ರ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'result': 'ಮಾಪನ', 'samples': '예제들', 'client': 'ಕ್ಲೈಂಟ್', 'line': 'ಸಾಲು', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'work': '작업경로', 'x': 'x_ಸಮಭಾಜಕ', 'python_checks': '파이썬검사', 'download': 'ಡೌನ್_ಲೋಡ್', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'content': 'ವಿಷಯ_ಮೌಲ್ಯ', 'block': 'ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು', 'marker': '확인표시', 'command': 'ಆಜ್ಞೆ', 'expected': '예상결과', 'shell': 'ಶೆಲ್', 'drawing': 'ಚಿತ್ರರಚನೆ_ಹಾದಿ', 'f': 'ಫೈಲ್_ನಮೂದು', 'transcript': '대화기록', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'path': 'ಮಾರ್ಗ', 'screenshot': 'ಸ್ಕ್ರೀನ್_ಶಾಟ್', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ', 'cmd': '명령인수', 'name': 'ಹೆಸರು', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
