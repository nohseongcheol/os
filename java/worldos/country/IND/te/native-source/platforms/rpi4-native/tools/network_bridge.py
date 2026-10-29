#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/నెట్_వర్క్_బ్రిడ్జ్.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('నెట్_వర్క్_బ్రిడ్జ్', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('నెట్_వర్క్_బ్రిడ్జ్')
    대응 = {'response': '응답자료', 'parts': 'పథం_భాగం', 's': 'అక్షరసరం_డేటా', 'i': '순번', 'close': 'మూసివేయి', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ప్రవేశం_మూల్యం', 'flags': 'నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ', 'ftp_port': 'ఫైలు_బదిలీ_పోర్ట్_సంఖ్య', 'args': 'కారకం_శ్రేణి', 'server': 'సర్వర్_మూల్యం', 'data': 'డేటా', 'ethernet_input': '이더넷입력', 'trace_packet': 'జాడ_ప్యాకెట్', 'GATEWAY': '관문기계주소', 'rule': 'నియమం_మూల్యం', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'హోస్ట్', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'అతిథి', 'destination': 'గమ్యం_డేటా_ఇమెయిల్', 'ethernet_port': 'ఇథర్నెట్_పోర్టు', 'b': '둘째값', 'MAC': 'యంత్రం_ఇమెయిల్', 'arp': 'ఇమెయిల్_స్పష్టత_ప్యాకెట్', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'చక్రం_మూల్యం', 'port': 'పోర్ట్_సంఖ్య', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'readable': '읽을수있음', 'c': 'అక్షర_కోడ్', 'p': 'డేటా_స్థాయి', 'writers': '쓰기대상들', 'IP': 'ఇంటర్నెట్_చిరునామా_మూల్యం', 'e': '보조항목', 'n': '개수', 'packet': 'ప్యాకెట్_డేటా', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'నెట్_వర్క్_బ్రిడ్జ్', 'window': 'విండో', 'capture': 'సంగ్రహణ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
