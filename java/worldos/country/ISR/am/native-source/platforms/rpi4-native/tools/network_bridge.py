#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/መረብ_ድልድይ.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('መረብ_ድልድይ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('መረብ_ድልድይ')
    대응 = {'response': '응답자료', 'parts': 'ዱካ_አካል', 's': 'ኅብረቁምፊ_ውሂብ', 'i': '순번', 'close': 'መዝጊያ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ምዝግብ_እሴት', 'flags': 'ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት', 'ftp_port': 'ፋይል_ትልልፍ_የወደብ_ቁጥር', 'args': 'ነጋሪ_እሴት_ድርድር', 'server': 'አገልጋይ_እሴት', 'data': 'ውሂብ', 'ethernet_input': '이더넷입력', 'trace_packet': 'ዱካ_ፓኬት', 'GATEWAY': '관문기계주소', 'rule': 'ደንብ_እሴት', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'አዘጋጅ_b78e430d', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'እንግዳ', 'destination': 'መድረሻ_ውሂብ_አድራሻ', 'ethernet_port': 'ኢተርኔት_ወደብ', 'b': '둘째값', 'MAC': 'ማሽን_አድራሻ', 'arp': 'አድራሻ_ጥራት_ፓኬት', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ዑደት_እሴት', 'port': 'የወደብ_ቁጥር', 'offset': 'ዝንፍ_እሴት', 'readable': '읽을수있음', 'c': 'የቁምፊ_ኮድ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'writers': '쓰기대상들', 'IP': 'የበይነመረብ_አድራሻ_እሴት', 'e': '보조항목', 'n': '개수', 'packet': 'ፓኬት_ውሂብ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'መረብ_ድልድይ', 'window': 'መስኮት', 'capture': 'መያዝ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
