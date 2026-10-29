#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ರಚಿಸು_ಇಮೇಜ್.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ರಚಿಸು_ಇಮೇಜ್', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ರಚಿಸು_ಇಮೇಜ್')
    대응 = {'total': '총량', 'start': 'ಚಲಾಯಿಸು_2', 'firmware': '기초제어프로그램', 'files': 'ಫೈಲ್_ಪಟ್ಟಿ', 'archive_base': '압축기준', 'partition': 'ವಿಭಜನೆ_ಫೈಲ್', 'archive': 'ಅರ್ಖೀವ್', 'main': 'ಚಲಾಯಿಸು_2', 'block': 'ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'boot': '부팅경로', 'stage': 'ಹಂತ_ಮೌಲ್ಯ', 'out': 'ಮಾಪನ_ಡೇಟಾ', 'expected': '예상결과', 'f': 'ಫೈಲ್_ನಮೂದು', 'src': '원본주소', 'path': 'ಮಾರ್ಗ', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'extracted': '추출자료', 'member': 'ಸದಸ್ಯ', 'mbr': '주부트기록', 'image': 'ಇಮೇಜ್', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ಪರವಾನಗಿ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'value': 'ಮೌಲ್ಯ', 'manifest': '꾸러미명세', 'dest': 'ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
