#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ')
    대응 = {'timeout': '시간제한', 's': 'ᎠᏍᏘ_ᎦᏟᏌᏅᎯ', 'i': '순번', 'match': '일치', 'files': 'ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ', 'program': 'ᎬᏙᏗ', 'executable': '실행가능파일', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'chunk': '조각', 'data': 'ᎦᏟᏌᏅᎯ', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'send': 'ᏫᎦᏅᏗ', 'main': 'ᎠᎢᏎᏍᏗ', 'marker': '확인표시', 'command': 'ᎤᏁᏤᎸᎩ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', 'p': '자료위치', 'parser': '인수해석기', 'options': 'ᎠᏑᏰᏍᏗᎢ', 'kind': 'ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ', 'selector': 'ᎠᏑᏰᏍᎩ', 'upload_data': 'ᏫᏢᎦ_ᎦᏟᏌᏅᎯ', 'end': '끝위치', 'n': '개수', 'd': 'ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ', 'key': '누름값', 'output': '출력결과', 'line': 'ᏚᏓᏅᏅᎢ', 'name': 'ᏚᏙᎥᎢ', 'upload_name': 'ᏫᏢᎦ_ᏚᏙᎥᎢ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
