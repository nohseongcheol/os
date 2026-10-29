#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/통신다리.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'መገዲ_ክፍሊ_ኣካል', 's': 'ሕብረ_ቁምፊ_ሓበሬታ', 'i': '순번', 'close': 'ዕጸው', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ምእታው_ዋጋ', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'server': 'ኣገልጋሊ_ዋጋ', 'data': 'ሓበሬታ', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'ሕጊ_ዋጋ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'አዐንግድ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'መዓልቦ_ሓበሬታ_ኣድራሻ', 'ethernet_port': 'ብገመድ_ልጉብ_መርበብ_ወደብ', 'b': '둘째값', 'MAC': 'ማሽን_ኣድራሻ', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ዙር_ዋጋ', 'port': '접속번호', 'offset': 'ሽፋን_ዋጋ', 'readable': '읽을수있음', 'c': 'ኮድ_ፊደል', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'ናይ_መርበብ_ኣድራሻ_ዋጋ', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'መስኮት', 'capture': 'ቕረጽ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
