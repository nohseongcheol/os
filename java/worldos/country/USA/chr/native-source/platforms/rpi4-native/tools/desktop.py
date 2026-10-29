#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ᎦᎵᏓᏍᏔᏅ', 'exact': '정확한값', 'network': 'ᏧᎾᏚᏓᎵ', 'closed': '닫힘', 'length': 'ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ', 'resources': 'ᏗᏓᏁᏢᎢ', 'data': 'ᎦᏟᏌᏅᎯ', 'shift': 'SHIFT_ᏍᏚᎢᏍᏗ', 'send': 'ᏫᎦᏅᏗ', 'run_desktop': 'ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ᎠᏁᏢᏍᎩ', 'text': 'ᎠᎪᎵᏰᏗ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ', 'tail': '끝부분', 'size': 'ᎢᎩᏓ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ᎠᏥᏍᏕᎵᏍᎩ', 'char': 'ᎪᏪᎸ_ᎦᏟᏌᏅᎯ', 'work': '작업경로', 'Keyboard': 'ᏗᏐᏅᏍᏙᏗ', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'Desktop': 'ᎫᏓᎳ_ᎦᏍᎩᎶᎩ_ᎦᏚ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ', 'command': 'ᎤᏁᏤᎸᎩ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'cp': 'ᎪᏪᎸ_ᎪᏗᏍᎩ', 'terminate': '종료시키기', 'security': 'ᎤᎦᏎᏍᏗ', 'vnc_port': '원격화면접속번호', 'body': '본문', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': 'ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ᏗᎪᎵᏰᏍᎩ', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
