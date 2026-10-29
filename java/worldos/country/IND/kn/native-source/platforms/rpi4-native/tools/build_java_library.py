#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ಶಿರೋಲೇಖ_ಮೌಲ್ಯ', 'sources': '원문목록', 'i': '순번', 'info': 'ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ', 'payload': 'ಪೇಲೋಡ್_ಡೇಟಾ', 'src': '원본주소', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ವರ್ಗ_ಹಾದಿ', 'dist': '배포경로', 'archive': 'ಅರ್ಖೀವ್', 'output': '출력결과', 'root': 'ಮೂಲ_ಇಮೇಲ್', 'name': 'ಹೆಸರು', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
