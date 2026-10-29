#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/예제되돌림서버.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'ഡാറ്റാ', 'sock': '소켓', 'tcp_port': 'ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': 'കൈകാര്യംചെയ്യല്_കണക്ഷൻ_HTTP_അപേക്ഷ', 'EchoServers': '되돌림서버', 'parser': 'പാഴ്_സർ', 'server': 'സെര്_വര്_മൂല്യം', 'udp_port': '전문접속번호', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
