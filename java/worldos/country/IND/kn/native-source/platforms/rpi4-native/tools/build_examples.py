#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/예제빌드.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ಮಾಪನ_ಡೇಟಾ', 'build_examples': '예제만들기', 'files': 'ಫೈಲ್_ಪಟ್ಟಿ', 'java': '자바실행', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'path': 'ಮಾರ್ಗ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'readme': 'README_ಫೈಲ್', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ನೋಡುವ_ಪದಸೂಚಿ', 'classes': 'ವರ್ಗ_ಹಾದಿ', 'repo': 'ಸಂಗ್ರಹಣೆ_ಹಾದಿ', 'root': 'ಮೂಲ_ಇಮೇಲ್', 'content': 'ವಿಷಯ_ಮೌಲ್ಯ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'target': 'ಲಕ್ಷ್ಯ', 'manifest': '꾸러미명세', 'language': 'ಭಾಷೆ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
