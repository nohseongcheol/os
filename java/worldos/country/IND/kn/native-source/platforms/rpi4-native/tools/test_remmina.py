#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/원격한글시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ಚಲಾಯಿಸು_2', 'profile': 'ಪ್ರೊಫೈಲ್', 'focused': 'ಕೇಂದ್ರೀಕೃತ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ಸರ್ವರ್_ಮೌಲ್ಯ', 'log': 'ಲಾಗ್_ದಾಖಲೆ', 'args': 'ವಾದ_ಅರೇ', 'deadline': '마감시각', 'data': 'ಡೇಟಾ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ಚಲಾಯಿಸು_2', 'ready': '준비완료', 'found': 'ಶೋಧ_ಮಾಪನ', 'guest': 'ಅತಿಥಿ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'marker': '확인표시', 'text': 'ಪಠ್ಯ', 'out': 'ಮಾಪನ_ಡೇಟಾ', 'env': '환경', 'f': 'ಫೈಲ್_ನಮೂದು', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'version': '판번호', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'selector': 'ಸೆಲೆಕ್ಟರ್', 'xvfb': 'ಅಗೋಚರ_ಪ್ರದರ್ಶನ', 'display': 'ಪ್ರದರ್ಶನ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ಹೆಸರು', 'window': 'ವಿಂಡೋ', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
