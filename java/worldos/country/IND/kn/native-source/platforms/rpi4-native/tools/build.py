#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ')
    대응 = {'network': 'ನೆಟ್_ವರ್ಕ್', 'BUILD': 'ಬಿಲ್ಡ್_ಹಾದಿ', 'ar': 'ಅರ್ಖೀವ್_ಪರಿಕರ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ಫಾಂಟ್_ಡೇಟಾ', 'flags': 'ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ವಾದ_ಅರೇ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ವಿಧಾನ_ನಮೂದು', 'main': 'ಚಲಾಯಿಸು_2', 'objcopy': 'ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಕನ್ವರ್ಟರ್', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ರಚಿಸು_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್', 'f': 'ಫೈಲ್_ನಮೂದು', 'extra': '추가영역', 'exports': 'ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ', 'jobs': '빌드작업', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'path': 'ಮಾರ್ಗ', 'REPO': 'ಸಂಗ್ರಹಣೆ_ಮೂಲ', 'tool': 'ಪರಿಕರಗಳು', 'classes': 'ವರ್ಗ_ಹಾದಿ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ಚಿಹ್ನೆ_ಮೌಲ್ಯ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'build_network': 'ರಚಿಸು_ನೆಟ್_ವರ್ಕ್_48d29d6d', 'font_info': 'ಫಾಂಟ್_ಮಾಹಿತಿ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
