#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು')
    대응 = {'data': 'ಡೇಟಾ', 'i': '순번', 'name': 'ಹೆಸರು', 'c': 'ಅಕ್ಷರ_ಕೋಡ್', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'args': 'ವಾದ_ಅರೇ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
