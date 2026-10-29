#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/예제되돌림서버.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'தரவு', 'sock': '소켓', 'tcp_port': 'டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': 'நடத்தி_இணைப்பு_HTTP_வேண்டுதல்', 'EchoServers': '되돌림서버', 'parser': 'பார்சர்', 'server': 'சேவையகம்_மதிப்பு', 'udp_port': '전문접속번호', 'args': 'மதிப்புரு_கோவை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
