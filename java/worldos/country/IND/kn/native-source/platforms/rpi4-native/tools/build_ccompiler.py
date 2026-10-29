#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ಮಾಪನ_ಡೇಟಾ', 'builtins': '내장연산', 'header': 'ಶಿರೋಲೇಖ_ಮೌಲ್ಯ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'flags': 'ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ', 'path': 'ಮಾರ್ಗ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'cc': '시언어번역기', 'obj': 'ತಲುಪುವ_ಫೈಲ್', 'flag': 'ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ', 'ld': '연결편집기', 'objects': 'ಗಮ್ಯಸ್ಥಾನ_ಫೈಲ್_ಗಳು', 'repo': 'ಸಂಗ್ರಹಣೆ_ಹಾದಿ', 'v': '임시값', 'upstream': 'ಅಪ್_ಸ್ಟ್ರೀಮ್', 'root': 'ಮೂಲ_ಇಮೇಲ್', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ಹೆಸರು', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
