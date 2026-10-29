#!/usr/bin/env python3
"""기존 ಮಾರ್ಗ 호환 ನಮೂದು_ಬಿಂದು. ನಿಜವಾದ_ಡೇಟಾ 구현: ../ಪರಿಕರಗಳು/ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ.py"""
import importlib as 가져오기
import sys as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ
from pathlib import Path as ಮಾರ್ಗ
ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಮೌಲ್ಯ.path.insert(0, str(ಮಾರ್ಗ(__file__).resolve().parents[1] / 'ಪರಿಕರಗಳು'))
if __name__ == '__main__':
    import runpy as ಅಪ್ಲಿ_ಲಾಂಚರ್
    ಅಪ್ಲಿ_ಲಾಂಚರ್.run_module('ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ')
    대응 = {'response': '응답자료', 'parts': 'ಹಾದಿ_ಘಟಕ', 's': 'ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ', 'i': '순번', 'close': 'ಮುಚ್ಚು', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ನಮೂದು_ಮೌಲ್ಯ', 'flags': 'ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ', 'ftp_port': 'ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'args': 'ವಾದ_ಅರೇ', 'server': 'ಸರ್ವರ್_ಮೌಲ್ಯ', 'data': 'ಡೇಟಾ', 'ethernet_input': '이더넷입력', 'trace_packet': 'ಟ್ರೇಸ್_ಪ್ಯಾಕೆಟ್', 'GATEWAY': '관문기계주소', 'rule': 'ನಿಯಮ_ಮೌಲ್ಯ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ಹೋಸ್ಟ್', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'ಅತಿಥಿ', 'destination': 'ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್', 'ethernet_port': 'ಇಥರ್ನೆಟ್_ಪೋರ್ಟ್', 'b': '둘째값', 'MAC': 'ಯಂತ್ರ_ಇಮೇಲ್', 'arp': 'ಇಮೇಲ್_ರಿಸೊಲ್ಯೂಶನ್_ಪ್ಯಾಕೆಟ್', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ಆವರ್ತನೆ_ಮೌಲ್ಯ', 'port': 'ಪೋರ್ಟ್_ಸಂಖ್ಯೆ', 'offset': 'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ', 'readable': '읽을수있음', 'c': 'ಅಕ್ಷರ_ಕೋಡ್', 'p': 'ಡೇಟಾ_ಹುದ್ದೆ', 'writers': '쓰기대상들', 'IP': 'ಇಂಟರ್ನೆಟ್_ವಿಳಾಸ_ಮೌಲ್ಯ', 'e': '보조항목', 'n': '개수', 'packet': 'ಪ್ಯಾಕೆಟ್_ಡೇಟಾ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ', 'window': 'ವಿಂಡೋ', 'capture': 'ಸೆರೆಹಿಡಿ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
