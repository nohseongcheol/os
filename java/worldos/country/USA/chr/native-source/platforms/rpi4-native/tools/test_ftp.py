#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᏓᎪᎵᏰᏍᎩ_FTP.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᏓᎪᎵᏰᏍᎩ_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᏓᎪᎵᏰᏍᎩ_FTP')
    대응 = {'timeout': '시간제한', 'payload': 'ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ᎦᏟᏌᏅᎯ', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ᎠᏍᏆᏂᎪᏛᎢ', 'main': 'ᎠᎢᏎᏍᏗ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ᎾᏓᏅᏍᎬᎾ_ᎦᏟᏌᏅᎯ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ᎤᏁᏤᎸᎩ', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'ᏗᏯᏙᎯᎯ_ᎦᏟᏌᏅᎯ', 'shell': 'ᎤᏯᏍᎦ', 'upload': '올리기', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'ᎠᏑᏰᏍᎩ', 'end': '끝위치', 'e': '보조항목', 'ftp': 'ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ', 'result': '결과', 'unchanged': '보존자료', 'line': 'ᏚᏓᏅᏅᎢ', 'server_tcp_port': 'ᏗᏯᏙᎯᎯ_ᎤᏪᎬ_ᎫᏓᎸᏗ', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
