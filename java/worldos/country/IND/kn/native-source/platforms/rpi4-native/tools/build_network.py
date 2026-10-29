#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ನೆಟ್_ವರ್ಕ್.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಬಿಲ್ಡ್_ನೆಟ್_ವರ್ಕ್', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಬಿಲ್ಡ್_ನೆಟ್_ವರ್ಕ್')
    대응 = {'obj': 'ತಲುಪುವ_ಫೈಲ್', 'objects': 'ಗಮ್ಯಸ್ಥಾನ_ಫೈಲ್_ಗಳು', 'library': 'ಲೈಬ್ರರಿ', 'output': '출력결과', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'root': 'ಮೂಲ_ಇಮೇಲ್', 'files': 'ಫೈಲ್_ಪಟ್ಟಿ', 'source': '원본자료', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'flags': 'ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ', 'path': 'ಮಾರ್ಗ', 'build_network': 'ರಚಿಸು_ನೆಟ್_ವರ್ಕ್_48d29d6d', 'cc': '시언어번역기', 'ar': 'ಅರ್ಖೀವ್_ಪರಿಕರ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
