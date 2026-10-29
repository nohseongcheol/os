#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/창시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_ಸಮಭಾಜಕ', 's': 'ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ', 'xy': 'ಕೊ_ಆರ್ಡಿನೆಟ್_ಪೇರ್', 'sel': 'ಸೆಲೆಕ್ಟರ್_a916db4e', 'seconds': '초단위', 'log': 'ಲಾಗ್_ದಾಖಲೆ', 'at': '현재위치', 'send': 'ಕಳುಹಿಸಿ', 'main': 'ಚಲಾಯಿಸು_2', 'req': '요청값', 'hot': 'ಕಿರುಹಾದಿ_ಮೌಲ್ಯ', 'pump': 'ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'marker': '확인표시', 'b': '둘째값', 'command': 'ಆಜ್ಞೆ', 'shell': 'ಶೆಲ್', 'f': 'ಫೈಲ್_ನಮೂದು', 'color': '색상', 'click': 'ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್', 'k': '셋째순번', 'c': 'ಅಕ್ಷರ_ಕೋಡ್', 'r': '반환값', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'done': '완료량', 'end': 'ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್', 'command_mode': 'ಆದೇಶ_ಮೋಡ್', 'key': '누름값', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'pixels': '화소들', 'result': 'ಮಾಪನ', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'dest': 'ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
