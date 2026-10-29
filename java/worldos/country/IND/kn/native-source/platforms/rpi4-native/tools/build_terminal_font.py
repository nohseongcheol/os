#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ಟರ್ಮಿನಲ್_ಫಾಂಟ್.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಬಿಲ್ಡ್_ಟರ್ಮಿನಲ್_ಫಾಂಟ್', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಬಿಲ್ಡ್_ಟರ್ಮಿನಲ್_ಫಾಂಟ್')
    대응 = {'data': 'ಡೇಟಾ', 'img': 'ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ', 'bits': 'ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ_ಪಟ್ಟಿ', 'x': 'x_ಸಮಭಾಜಕ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ಹಾದಿ_ಪಟ್ಟಿ', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'main': 'ಚಲಾಯಿಸು_2', 'src': '원본주소', 'fonts': 'ಫಾಂಟ್_ಪಟ್ಟಿ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'cp': 'ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್', 'target': 'ಲಕ್ಷ್ಯ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
