#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/டெஸ்க்டாப்_காட்சி.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('டெஸ்க்டாப்_காட்சி', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('டெஸ்க்டாப்_காட்சி')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'பிழை', 'exact': '정확한값', 'network': 'பிணையம்', 'closed': '닫힘', 'length': 'நீளம்_மதிப்பு', 'opened': '열림', 'ftp_port': 'கோப்பு_இடமாற்று_முனைய_எண்', 'server': 'சேவையகம்_மதிப்பு', 'resources': 'ஆதாரங்கள', 'data': 'தரவு', 'shift': 'SHIFT_விசை', 'send': 'அனுப்பு', 'run_desktop': 'இயக்கு_டெஸ்க்டாப்', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ஓம்பு', 'text': 'உரை', 'korean': '한글여부', 'port': 'முனைய_எண்', 'signum': '신호번호', 'version': 'பதிப்புரு_எண்', 'parser': 'பார்சர்', 'bridge': 'பிரிட்ஜ்', 'kind': 'வகை_மதிப்பு_4b6d6445', 'tail': '끝부분', 'size': 'அளவு', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_பொத்தான்_அச்சுத்_தொகுப்பு', 'prefix': '앞부분', 'client': 'பயனகம்', 'char': 'எழுத்துருத்_தரவு', 'work': '작업경로', 'Keyboard': 'விசைப்பலகை', 'x': 'x_ஒத்ததரமுள்ளது', 'down': '누르는중', 'net': 'பிணையம்_பிரிட்ஜ்_உள்ளீடு', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'மதிப்புரு_கோவை', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'செயல்பாடு', 'Desktop': 'இணை_டெஸ்க்டாப்', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'சுவிட்ச்_பயன்முறை', 'command': 'கட்டளை', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_விசை', 'path': 'பாதை_2', 'cp': 'எழுத்துக்குறி_குறியீட்டு_முறை', 'terminate': 'முடி', 'security': 'பாதுகாப்பு', 'vnc_port': '원격화면접속번호', 'body': 'தகவல்_உரை', 'index': 'தேடுதல்_அடைவு', 'exited': '종료됨', 'keysym': 'சாவி_சின்னம்', 'output': '출력결과', 'keyboard': 'விசைப்பலகை_உள்ளீடு', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'படிப்பவர்', 'NetworkBridge': 'பிணையம்_பிரிட்ஜ்', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
