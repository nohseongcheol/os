#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/பிணையம்_பிரிட்ஜ்.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('பிணையம்_பிரிட்ஜ்', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('பிணையம்_பிரிட்ஜ்')
    대응 = {'response': '응답자료', 'parts': 'பாதை_உபகரணம்', 's': 'சரம்_தரவு', 'i': '순번', 'close': 'மூடு', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'உள்ளீடு_மதிப்பு', 'flags': 'உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை', 'ftp_port': 'கோப்பு_இடமாற்று_முனைய_எண்', 'args': 'மதிப்புரு_கோவை', 'server': 'சேவையகம்_மதிப்பு', 'data': 'தரவு', 'ethernet_input': '이더넷입력', 'trace_packet': 'சுவடு_பாக்கெட்', 'GATEWAY': '관문기계주소', 'rule': 'விதி_மதிப்பு', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ஓம்பு', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'விருந்தினர்', 'destination': 'இலக்கு_தரவு_முகவரி', 'ethernet_port': 'ஈத்தர்நெட்_முணையம்', 'b': '둘째값', 'MAC': 'இயந்திரம்_முகவரி', 'arp': 'முகவரி_தெளிவுத்திறன்_பாக்கெட்', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'சுற்று_மதிப்பு', 'port': 'முனைய_எண்', 'offset': 'ஆஃப்செட்_மதிப்பு', 'readable': '읽을수있음', 'c': 'எழுத்துக்குறி_குறியீடு', 'p': 'தரவு_நிலை', 'writers': '쓰기대상들', 'IP': 'இணைய_முகவரி_மதிப்பு', 'e': '보조항목', 'n': '개수', 'packet': 'பாக்கெட்_தரவு', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'பிணையம்_பிரிட்ஜ்', 'window': 'சாளரம்', 'capture': 'பிடிப்பு'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
