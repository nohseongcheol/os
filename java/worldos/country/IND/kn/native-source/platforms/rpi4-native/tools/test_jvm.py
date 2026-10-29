#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ', 'actual': 'ನಿಜವಾದ_ಮಾಪನ', 'match': '일치', 'payload': 'ಪೇಲೋಡ್_ಡೇಟಾ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ಚಲಾಯಿಸು_2', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ವರ್ಗ_ಹಾದಿ', 'output': '출력결과', 'result': 'ಮಾಪನ', 'cmd': '명령인수', 'name': 'ಹೆಸರು', 'jar': '자바꾸러미', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
