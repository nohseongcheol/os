#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/예제시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'දත්ත', 'graphics_command': '그림명령', 'main': 'ක්_රියාත්මක_කරන්න_2', 'row': '행위치', 'init': '초기값', 'target': 'ඉලක්කය', 'ROOT': '기준', 'text': 'පෙළ', 'binary': 'ද්විමය', 'out': '결과자료', 'entry': 'පිවිසුම_ලකුණ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'ඇරඹුම_චිත්_රය', 'col': '열위치', 'begin': 'ඇරඹුම_ඕෆ්සෙට්', 'kind': 'ප්_රවර්ගය_අගය', 'selector': 'වරකය', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'සේවාලාභීයා', 'line': 'පේළිය', 'report': 'වලංගුකරණය_වාර්තාව', 'language': 'භාෂාව', 'x': 'x_ඛණ්ඩාංකය', 'start': 'ක්_රියාත්මක_කරන්න_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ඊමේල්_ලැයිස්තුව', 'payload': 'ගෙවීම්_භාරය_දත්ත', 'proc': 'සැකසුම', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'නම_වගුව', 'content': 'අන්තර්ගතය_අගය', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ගොනුව_පිවිසුම_නම', 'shell': 'කවචය', 'color': '색상', 'transcript': '대화기록', 'offset': 'ඕෆ්සෙට්_අගය', 'h': '높이값', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'c': 'අනුලකුණු_කේතය', 'path': 'මාර්_ගය', 'encoding': 'අනුලකුණු_කුලකය', 'end': 'නිමා_කරන්න_ඕෆ්සෙට්', 'ftp': 'ගොනුව_මාරුව_සබැඳුම', 'pixels': '화소들', 'symbol': 'සංකේතය_අගය', 'source': '원본자료', 'name': 'නම', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
