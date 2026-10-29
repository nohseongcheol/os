#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/통신다리.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'ផ្លូវ_សមាសភាគ', 's': 'សំនុំអក្សរ_ទិន្នន័យ', 'i': '순번', 'close': 'បិទ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ការបញ្ចូល_តំលៃ', 'flags': 'ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ', 'ftp_port': 'ឯកសារ_ផ្ទេរ_លេខរន្ធ', 'args': 'អាគុយម៉ង់_អារេ', 'server': 'ម៉ាស៊ីនមេ_តំលៃ', 'data': 'ទិន្នន័យ', 'ethernet_input': '이더넷입력', 'trace_packet': 'ត្រេស_កញ្ចប់', 'GATEWAY': '관문기계주소', 'rule': 'តម្រង_តំលៃ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ហូស', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'ភ្ញៀវ', 'destination': 'ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': 'ម៉ាស៊ីន_អ៊ីម៉ែល', 'arp': 'អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'វដ្ដ_តំលៃ', 'port': 'លេខរន្ធ', 'offset': 'ការបែង_ភាគ_តំលៃ', 'readable': '읽을수있음', 'c': 'កូដនៃតួអក្សរ', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'writers': '쓰기대상들', 'IP': 'អាសយដ្ឋានអ៊ីនធឺណិត_តំលៃ', 'e': '보조항목', 'n': '개수', 'packet': 'កញ្ចប់_ទិន្នន័យ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'វីនដូ', 'capture': 'ថត'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
