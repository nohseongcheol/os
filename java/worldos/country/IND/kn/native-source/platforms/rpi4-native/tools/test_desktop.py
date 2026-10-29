#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/바탕화면시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ಸಮಭಾಜಕ', 'typing': '글자입력', 'message': '알림문', 'start': 'ಚಲಾಯಿಸು_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ಚಿಹ್ನೆ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'data': 'ಡೇಟಾ', 'main': 'ಚಲಾಯಿಸು_2', 'w': '너비값', 'init': '초기값', 'block': 'ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'marker': '확인표시', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'until': '까지', 'clipboard': 'ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ', 'dst': 'ಗಮ್ಯಸ್ಥಾನ_ಇಮೇಲ್', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'h': '높이값', 'src': '원본주소', 'event': 'ಸಂಗತಿ', 'encoding': 'ಅಕ್ಷರ_ಸಮೂಹ', 'size': 'ಗಾತ್ರ', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'output': '출력결과', 'symbol': 'ಚಿಹ್ನೆ_ಮೌಲ್ಯ', 'client': 'ಕ್ಲೈಂಟ್', 'char': 'ಅಕ್ಷರ_ಡೇಟಾ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
