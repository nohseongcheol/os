#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'ಮಾಪನ_ಡೇಟಾ', 'obj': 'ತಲುಪುವ_ಫೈಲ್', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ಅರ್ಖೀವ್', 'main': 'ಚಲಾಯಿಸು_2', 'posix': '포직스경로', 'files': 'ಫೈಲ್_ಪಟ್ಟಿ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'target': 'ಲಕ್ಷ್ಯ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'destination': 'ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
