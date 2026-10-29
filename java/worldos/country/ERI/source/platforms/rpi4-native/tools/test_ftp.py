#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/파일전송시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ጽዕነት_ክፍሊት_ሓበሬታ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ሓበሬታ', 'proc': 'መስርሕ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ሰንድ', 'main': 'ኣኺድ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ቀዋሚ_ምንጪ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'ጽሑፍ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ትእዛዝ', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'ኣገልጋሊ_ምንጪ', 'shell': 'ሽፋን', 'upload': 'ስቐል_ፋይላት', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'መራፂ', 'end': 'ኣቑም_ሽፋን', 'e': '보조항목', 'ftp': 'ፋይል_ምስጋር_ርክብ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'መዘና_ዋጋ', 'result': '결과', 'unchanged': '보존자료', 'line': 'መስመር', 'server_tcp_port': 'ኣገልጋሊ_ወሓዚ_ወደብ', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ምርግጋፅ_ጸብጻብ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
