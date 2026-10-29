#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/डेस्कटप_दृश्य.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('डेस्कटप_दृश्य', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('डेस्कटप_दृश्य')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'त्रुटि', 'exact': '정확한값', 'network': 'सञ्जाल', 'closed': '닫힘', 'length': 'लम्बाइ_मान', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'सर्भर_मान', 'resources': 'संसाधनहरू', 'data': 'लगत', 'shift': 'SHIFT_कुञ्जी', 'send': 'पठाउनुहोस्', 'run_desktop': 'चलाउनुहोस्_डेस्कटप', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'होस्ट', 'text': 'पाठ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ब्रिज', 'kind': 'कोटि_मान', 'tail': '끝부분', 'size': 'आकार', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ग्राहक', 'char': 'वर्ण_लगत', 'work': '작업경로', 'Keyboard': 'कुञ्जीपाटी', 'x': 'x_समन्वय', 'down': '누르는중', 'net': 'सञ्जाल_ब्रिज_प्रविष्टि', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'तर्क_विन्यास', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'प्रक्रिया', 'Desktop': 'कनेक्ट_डेस्कटप', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'परिवर्तन_मोड', 'command': 'आदेश', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_कुञ्जी', 'path': 'मार्ग', 'cp': 'वर्ण_एनकोडिङ', 'terminate': '종료시키기', 'security': 'सुरक्षा', 'vnc_port': '원격화면접속번호', 'body': 'मुख्य_पाठ', 'index': 'विवरण_हेर्ने_सुविधा_अनुक्रमणिका', 'exited': '종료됨', 'keysym': 'कुञ्जी_चिन्ह', 'output': '출력결과', 'keyboard': 'कुञ्जीपाटी_प्रविष्टि', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'पाठक', 'NetworkBridge': 'सञ्जाल_ब्रिज', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
