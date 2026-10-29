#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಪೂರೈಸು_ಆದೇಶ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಪೂರೈಸು_ಆದೇಶ')
    대응 = {'supported': '지원목록', 'parser': 'ಪಾರ್ಸರ್', 'qemu': '모의기계', 'run_desktop': 'ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್', 'main': 'ಚಲಾಯಿಸು_2', 'host': 'ಹೋಸ್ಟ್', 'status': 'ಸ್ಥಿತಿ_ಮೌಲ್ಯ', 'NetworkBridge': 'ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'bridge': 'ಸೇತುವೆ', 'loader': '적재기', 'base': 'ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ', 'options': 'ಆಯ್ಕೆಗಳು', 'binary': 'ದ್ವಿಮಾನ', 'args': 'ವಾದ_ಅರೇ', 'command': 'ಆಜ್ಞೆ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
