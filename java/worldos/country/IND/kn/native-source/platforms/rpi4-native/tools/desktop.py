#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ದೋಷ', 'exact': '정확한값', 'network': 'ನೆಟ್_ವರ್ಕ್', 'closed': '닫힘', 'length': 'ಉದ್ದ_ಮೌಲ್ಯ', 'opened': '열림', 'ftp_port': 'ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'server': 'ಸರ್ವರ್_ಮೌಲ್ಯ', 'resources': 'ಸಂಪನ್ಮೂಲಗಳು', 'data': 'ಡೇಟಾ', 'shift': 'SHIFT_ಕೀಲಿ', 'send': 'ಕಳುಹಿಸಿ', 'run_desktop': 'ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ಹೋಸ್ಟ್', 'text': 'ಪಠ್ಯ', 'korean': '한글여부', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'signum': '신호번호', 'version': '판번호', 'parser': 'ಪಾರ್ಸರ್', 'bridge': 'ಸೇತುವೆ', 'kind': 'ವರ್ಗ_ಮೌಲ್ಯ', 'tail': '끝부분', 'size': 'ಗಾತ್ರ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_ಬಟನ್_ಸಮನ್ವಯ', 'prefix': '앞부분', 'client': 'ಕ್ಲೈಂಟ್', 'char': 'ಅಕ್ಷರ_ಡೇಟಾ', 'work': '작업경로', 'Keyboard': 'ಕೀಲಿಮಣೆ', 'x': 'x_ಸಮಭಾಜಕ', 'down': '누르는중', 'net': 'ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ವಾದ_ಅರೇ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ಪ್ರಕ್ರಿಯೆ', 'Desktop': 'ಕನೆಕ್ಟ್_ಡೆಸ್ಕ್_ಟಾಪ್', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ಸ್ವಿಚ್_ಮಾಡಿ_ಮೋಡ್', 'command': 'ಆಜ್ಞೆ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ಕೀಲಿ', 'path': 'ಮಾರ್ಗ', 'cp': 'ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್', 'terminate': '종료시키기', 'security': 'ಭದ್ರತೆ', 'vnc_port': '원격화면접속번호', 'body': 'ಮುಖ್ಯ_ಪಠ್ಯ', 'index': 'ನೋಡುವ_ಪದಸೂಚಿ', 'exited': '종료됨', 'keysym': 'ಕೀ_ಚಿಹ್ನೆ', 'output': '출력결과', 'keyboard': 'ಕೀಲಿಮಣೆ_ನಮೂದು', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ಓದುಗ', 'NetworkBridge': 'ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
