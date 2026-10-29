#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/파일전송시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'የክፍያ_ጫና_ውሂብ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ውሂብ', 'proc': 'ሂደቶች', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ከዝን', 'main': 'ማስኬጃ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'አይንቀሳቀሴ_ምንጭ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ትእዛዝ', 'out': 'ልኬት_ውሂብ', 'expected': '예상결과', 'server_source': 'አገልጋይ_ምንጭ', 'shell': 'ሼል', 'upload': 'መጫን_ፋይሎች', 'transcript': '대화기록', 'port': 'የወደብ_ቁጥር', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ድልድይ', 'selector': 'መራጭ', 'end': 'ጨርስ_ዝንፍ', 'e': '보조항목', 'ftp': 'ፋይል_ትልልፍ_ግንኙነት', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'አቻ_እሴት', 'result': 'ልኬት', 'unchanged': '보존자료', 'line': 'መስመር', 'server_tcp_port': 'አገልጋይ_ልቀቅ_ወደብ', 'source': '원본자료', 'NetworkBridge': 'መረብ_ድልድይ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ማረጋገጥ_ዘገባ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
