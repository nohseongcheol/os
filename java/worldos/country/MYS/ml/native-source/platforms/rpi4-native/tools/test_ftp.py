#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/파일전송시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'പേലോഡ്_ഡാറ്റാ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ഡാറ്റാ', 'proc': 'പ്രക്രിയ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ശേഖരം', 'main': 'നടപ്പിലാക്കുക', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'സ്ഥിരമായ_ഉറവിടം', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ആജ്ഞ', 'out': 'അളവ്_ഡാറ്റാ', 'expected': '예상결과', 'server_source': 'സെര്_വര്_ഉറവിടം', 'shell': 'ഷെല്', 'upload': 'അപ്_ലോഡ്_ഫയലുകൾ', 'transcript': '대화기록', 'port': 'പോര്_ട്ട്_നമ്പര്', 'native': '자체실행파일', 'elf': 'നിര്_വ്വഹണക്ഷമമായ_ഫയല്', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ബ്രിഡ്_ജ്', 'selector': 'సెలక్టర్', 'end': 'അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്', 'e': '보조항목', 'ftp': 'ഫയല്_കൈമാറുക_കണക്ഷൻ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'പീര്_മൂല്യം', 'result': 'അളവ്', 'unchanged': '보존자료', 'line': 'ലൈൻ', 'server_tcp_port': 'സെര്_വര്_സ്ട്രീം_പോര്_ട്ട്', 'source': '원본자료', 'NetworkBridge': 'നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'నిర్ధారణ_నివేదిక'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
