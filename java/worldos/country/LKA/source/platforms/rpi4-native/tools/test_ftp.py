#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/파일전송시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ගෙවීම්_භාරය_දත්ත', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'දත්ත', 'proc': 'සැකසුම', 'code': 'උපදෙස_අනුක්_රමය', 'linux': '리눅스파일', 'archive': 'සංරක්ෂිතය', 'main': 'ක්_රියාත්මක_කරන්න_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ස්ථිතික_මූලය', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'පෙළ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'විධානය', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'සේවාදායකය_මූලය', 'shell': 'කවචය', 'upload': 'උඩුගත_කරන්න_ගොනු', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'පාලම', 'selector': 'වරකය', 'end': 'නිමා_කරන්න_ඕෆ්සෙට්', 'e': '보조항목', 'ftp': 'ගොනුව_මාරුව_සබැඳුම', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'සමානයා_අගය', 'result': '결과', 'unchanged': '보존자료', 'line': 'පේළිය', 'server_tcp_port': 'සේවාදායකය_දහර_තොට', 'source': '원본자료', 'NetworkBridge': 'ජාලය_පාලම', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'වලංගුකරණය_වාර්තාව'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
