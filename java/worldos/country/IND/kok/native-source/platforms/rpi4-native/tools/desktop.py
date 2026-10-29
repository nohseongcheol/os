#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/डॅस्कटॉप_दृश्य.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('डॅस्कटॉप_दृश्य', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('डॅस्कटॉप_दृश्य')
    대응 = {'count': 'प्रवेश_COUNT', 'special': '특수글쇠', 'error': 'चूक', 'exact': 'EXACT_मोल', 'network': 'नॅटवर्क', 'closed': '닫힘', 'length': 'लांबाय_मोल', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'सर्वर_मोल', 'resources': 'रिसोर्सीस', 'data': 'डेटा', 'shift': 'SHIFT_की', 'send': 'धाडचें', 'run_desktop': 'चलोवप_डॅस्कटॉप', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'येजमान', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ब्रिज', 'kind': 'वर्ग_मोल', 'tail': '끝부분', 'size': 'आवाठ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'क्लायंट', 'char': 'वर्ण_डेटा', 'work': '작업경로', 'Keyboard': 'किबोर्ड', 'x': 'x_coordinate', 'down': '누르는중', 'net': 'नॅटवर्क_ब्रिज_प्रवेश', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'युक्तीवाद_क्रम', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'प्रक्रिया', 'Desktop': 'कनॅक्ट_डॅस्कटॉप', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'स्विच_मोड', 'command': 'आदेश', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'पाथ', 'cp': 'वर्ण_एनकोडिंग', 'terminate': '종료시키기', 'security': 'सुरक्षा', 'vnc_port': '원격화면접속번호', 'body': 'देखीचो_उतारो', 'index': 'लूकअप_INDEX', 'exited': '종료됨', 'keysym': 'की_चिन्न', 'output': '출력결과', 'keyboard': 'किबोर्ड_प्रवेश', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'वाचक', 'NetworkBridge': 'नॅटवर्क_ब्रिज', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
