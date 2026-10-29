#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/파일전송시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'చెల్లింపుభారం_డేటా', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'డేటా', 'proc': 'క్రమణం', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ఆర్కైవ్', 'main': 'నడుపుము', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'నిశ్చల_మూలం', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ఆదేశము', 'out': 'ప్రమాణం_డేటా', 'expected': '예상결과', 'server_source': 'సర్వర్_మూలం', 'shell': 'షెల్', 'upload': 'అప్_లోడ్_ఫైల్_లు', 'transcript': '대화기록', 'port': 'పోర్ట్_సంఖ్య', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'బ్రిడ్జ్', 'selector': 'సెలక్టర్', 'end': 'ముగించు_ఆఫ్_సెట్', 'e': '보조항목', 'ftp': 'ఫైలు_బదిలీ_కనెక్షన్', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'పియర్_మూల్యం', 'result': 'ప్రమాణం', 'unchanged': '보존자료', 'line': 'పంక్తి', 'server_tcp_port': 'సర్వర్_ధార_పోర్టు', 'source': '원본자료', 'NetworkBridge': 'నెట్_వర్క్_బ్రిడ్జ్', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'నిర్ధారణ_నివేదిక'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
