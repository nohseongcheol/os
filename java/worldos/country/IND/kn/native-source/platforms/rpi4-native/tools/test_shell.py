#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/셸시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ಸಮಭಾಜಕ', 'msg': 'ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್', 'i': '순번', 'reply': 'ಪ್ರತ್ಯುತ್ತರ', 'call': '호출', 'args': 'ವಾದ_ಅರೇ', 'chunk': '조각', 'data': 'ಡೇಟಾ', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ಕಳುಹಿಸಿ', 'file': 'ಕಡತ', 'main': 'ಚಲಾಯಿಸು_2', 'found': 'ಶೋಧ_ಮಾಪನ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'marker': '확인표시', 'command': 'ಆಜ್ಞೆ', 'expected': '예상결과', 'pixel': 'ಪೆಲ್', 'shell': 'ಶೆಲ್', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್', 'image': 'ಇಮೇಜ್', 'key': '누름값', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'output': '출력결과', 'result': 'ಮಾಪನ', 'client': 'ಕ್ಲೈಂಟ್', 'line': 'ಸಾಲು', 'stream': 'ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ', 'name': 'ಹೆಸರು', 'value': 'ಮೌಲ್ಯ', 'receive': '수신하기', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
