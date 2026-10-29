#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ಡೇಟಾ', 'e': '보조항목', 'connection': 'ಸಂಪರ್ಕ_e05f319b', 'f': 'ಫೈಲ್_ನಮೂದು', 'peer': 'ಪೀರ್_ಮೌಲ್ಯ', 'self': '자신', 'udp': '전문제어', 't': 'ಟರ್ಮಿನಲ್_ನಮೂದು', 'tcp': 'ಸಂಪರ್ಕ_ನಿಯಂತ್ರಣ', 'EchoFixture': '되돌림시험서버', 'args': 'ವಾದ_ಅರೇ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
