#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏍᎩᎶᎩ_ᎦᏚ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏍᎩᎶᎩ_ᎦᏚ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏍᎩᎶᎩ_ᎦᏚ')
    대응 = {'x': '가로좌표', 'typing': '글자입력', 'message': '알림문', 'start': 'ᎠᎢᏎᏍᏗ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': '기호', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'data': 'ᎦᏟᏌᏅᎯ', 'main': 'ᎠᎢᏎᏍᏗ', 'w': '너비값', 'init': '초기값', 'block': 'ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'marker': '확인표시', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'until': '까지', 'clipboard': 'ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ', 'dst': 'ᏮᎦᏛᎢ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': '변위', 'h': '높이값', 'src': '원본주소', 'event': 'ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ', 'encoding': 'ᎪᏪᎸ_ᎤᎾᏓᏡᎬ', 'size': 'ᎢᎩᏓ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': '심볼', 'client': 'ᎠᏥᏍᏕᎵᏍᎩ', 'char': 'ᎪᏪᎸ_ᎦᏟᏌᏅᎯ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
