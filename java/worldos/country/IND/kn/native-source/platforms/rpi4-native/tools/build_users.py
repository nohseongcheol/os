#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಬಿಲ್ಡ್_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಬಿಲ್ಡ್_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್')
    대응 = {'mode': 'ವಿಧಾನ_ಮೋಡ್', 'header': 'ಶಿರೋಲೇಖ_ಮೌಲ್ಯ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ಅರ್ಖೀವ್_ಪರಿಕರ', 'posix': '포직스경로', 'payload': 'ಪೇಲೋಡ್_ಡೇಟಾ', 'flags': 'ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ಡೇಟಾ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'ಸಂಗ್ರಹಣೆ_ಹಾದಿ', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ಪಠ್ಯ', 'headers': 'ಶಿರೋಲೇಖ_ಪಟ್ಟಿ', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ಬಿಲ್ಡ್', 'build_users': 'ರಚಿಸು_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'text_address': 'ಆದೇಶ_ಇಮೇಲ್', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'path': 'ಮಾರ್ಗ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ', 'index': 'ನೋಡುವ_ಪದಸೂಚಿ', 'classes': 'ವರ್ಗ_ಹಾದಿ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ಡೇಟಾ_ಇಮೇಲ್', 'symbol': 'ಚಿಹ್ನೆ_ಮೌಲ್ಯ', 'root': 'ಮೂಲ_ಇಮೇಲ್', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ಹೆಸರು', 'value': 'ಮೌಲ್ಯ', 'fmt': 'ಸ್ವರೂಪ_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
