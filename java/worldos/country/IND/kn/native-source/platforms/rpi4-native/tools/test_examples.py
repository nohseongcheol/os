#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/예제시험.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'data': 'ಡೇಟಾ', 'graphics_command': 'ಗ್ರ್ಯಾಫಿಕ್ಸ್_ಆದೇಶ', 'main': 'ಚಲಾಯಿಸು_2', 'row': 'ಅಡ್ಡಸಾಲು_ಹುದ್ದೆ', 'init': '초기값', 'target': 'ಲಕ್ಷ್ಯ', 'ROOT': 'ಬಿಂಬಿಸು_ಮೂಲ', 'text': 'ಪಠ್ಯ', 'binary': 'ದ್ವಿಮಾನ', 'out': 'ಮಾಪನ_ಡೇಟಾ', 'entry': 'ನಮೂದು_ಬಿಂದು', 'got': '받은수', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'graphics_start': 'ಆರಂಭಿಸು_ಚಿತ್ರರಚನೆ', 'col': 'ಲಂಬಸಾಲು_ಹುದ್ದೆ', 'begin': 'ಆರಂಭಿಸು_ಆಫ್_ಸೆಟ್', 'kind': 'ವರ್ಗ_ಮೌಲ್ಯ', 'selector': 'ಸೆಲೆಕ್ಟರ್', 'n': '개수', 'key': '누름값', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'client': 'ಕ್ಲೈಂಟ್', 'line': 'ಸಾಲು', 'report': 'ದೃಢೀಕರಣ_ವರದಿ', 'language': 'ಭಾಷೆ', 'x': 'x_ಸಮಭಾಜಕ', 'start': 'ಚಲಾಯಿಸು_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ಕಳುಹಿಸಿ_ಪಟ್ಟಿ', 'payload': 'ಪೇಲೋಡ್_ಡೇಟಾ', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ಹೆಸರು_ಕೋಷ್ಟಕ', 'content': 'ವಿಷಯ_ಮೌಲ್ಯ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ಫೈಲ್_ನಮೂದು_ಹೆಸರು', 'shell': 'ಶೆಲ್', 'color': '색상', 'transcript': '대화기록', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'h': '높이값', 'run': 'ಪೂರೈಸು_ಆದೇಶ', 'c': 'ಅಕ್ಷರ_ಕೋಡ್', 'path': 'ಮಾರ್ಗ', 'encoding': 'ಅಕ್ಷರ_ಸಮೂಹ', 'end': 'ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್', 'ftp': 'ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ', 'pixels': '화소들', 'symbol': 'ಚಿಹ್ನೆ_ಮೌಲ್ಯ', 'source': '원본자료', 'name': 'ಹೆಸರು', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
