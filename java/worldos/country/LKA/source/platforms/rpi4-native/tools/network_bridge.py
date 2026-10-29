#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/ජාලය_පාලම.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('ජාලය_පාලම', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ජාලය_පාලම')
    대응 = {'response': '응답자료', 'parts': 'පෙත_සංරචකය', 's': 'අනුලකුණු_වැල_දත්ත', 'i': '순번', 'close': 'වසන්න', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'පිවිසුම_අගය', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'විස්තාරකය_ආරා_ව', 'server': 'සේවාදායකය_අගය', 'data': 'දත්ත', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'පෙරහන_අගය', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ධාරකය', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'අමුත්තා', 'destination': 'ගමනාන්තය_දත්ත_යොමුව', 'ethernet_port': 'ඊතර්නෙට්_තොට', 'b': '둘째값', 'MAC': 'යන්ත්_රය_යොමුව', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'චක්_රය_අගය', 'port': '접속번호', 'offset': 'ඕෆ්සෙට්_අගය', 'readable': '읽을수있음', 'c': 'අනුලකුණු_කේතය', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'අන්තර්ජාල_ලිපිනය_අගය', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ජාලය_පාලම', 'window': 'කවුළුව', 'capture': 'ග්_රහණය'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
