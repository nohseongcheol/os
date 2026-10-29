#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಪೂರೈಸು_ಫೈಲ್', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಪೂರೈಸು_ಫೈಲ್')
    대응 = {'timeout': '시간제한', 's': 'ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ', 'i': '순번', 'match': '일치', 'files': 'ಫೈಲ್_ಪಟ್ಟಿ', 'program': 'ಅಪ್ಲಿ', 'executable': '실행가능파일', 'args': 'ವಾದ_ಅರೇ', 'chunk': '조각', 'data': 'ಡೇಟಾ', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'send': 'ಕಳುಹಿಸಿ', 'main': 'ಚಲಾಯಿಸು_2', 'marker': '확인표시', 'command': 'ಆಜ್ಞೆ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'parser': 'ಪಾರ್ಸರ್', 'options': 'ಆಯ್ಕೆಗಳು', 'kind': 'ವರ್ಗ_ಮೌಲ್ಯ', 'selector': 'ಸೆಲೆಕ್ಟರ್', 'upload_data': 'ಅಪ್_ಲೋಡ್_ಡೇಟಾ', 'end': 'ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್', 'n': '개수', 'd': 'ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ', 'key': '누름값', 'output': '출력결과', 'line': 'ಸಾಲು', 'name': 'ಹೆಸರು', 'upload_name': 'ಅಪ್_ಲೋಡ್_ಹೆಸರು', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
