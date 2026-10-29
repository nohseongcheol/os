#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/실행파일시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ಮಾಪನ_ಡೇಟಾ', 'expected': '예상결과', 'phoff': 'ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'invalid': 'ಅಮಾನ್ಯ_ಡೇಟಾ', 'path': 'ಮಾರ್ಗ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ಮಾಪನ', 'format_': 'ಸ್ವರೂಪ_b87fd068', 'main': 'ಚಲಾಯಿಸು_2', 'content': 'ವಿಷಯ_ಮೌಲ್ಯ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'reference': 'ಹೋಲಿಕೆ_ಆಧಾರರೇಖೆ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'value': 'ಮೌಲ್ಯ', 'report': 'ದೃಢೀಕರಣ_ವರದಿ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
