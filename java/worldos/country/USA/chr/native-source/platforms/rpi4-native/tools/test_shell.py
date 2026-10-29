#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏯᏍᎦ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏯᏍᎦ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏯᏍᎦ')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'chunk': '조각', 'data': 'ᎦᏟᏌᏅᎯ', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ᏫᎦᏅᏗ', 'file': 'ᎠᏍᏆᏂᎪᏙᏗ', 'main': 'ᎠᎢᏎᏍᏗ', 'found': '찾은결과', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'marker': '확인표시', 'command': 'ᎤᏁᏤᎸᎩ', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'ᎤᏯᏍᎦ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': 'ᎤᏓᏴᎳᏛ', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'ᎠᏥᏍᏕᎵᏍᎩ', 'line': 'ᏚᏓᏅᏅᎢ', 'stream': 'ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ', 'name': 'ᏚᏙᎥᎢ', 'value': 'ᏧᎬᏩᎶᏗᏯ', 'receive': '수신하기', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
