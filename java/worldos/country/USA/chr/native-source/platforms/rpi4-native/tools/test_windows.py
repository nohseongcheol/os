#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᏓᎪᎵᏰᏍᎩ_Windows.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᏓᎪᎵᏰᏍᎩ_Windows', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᏓᎪᎵᏰᏍᎩ_Windows')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'ᎠᏍᏘ_ᎦᏟᏌᏅᎯ', 'xy': '좌표쌍', 'sel': 'ᎠᏑᏰᏍᎩ_a916db4e', 'seconds': '초단위', 'log': 'ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ', 'at': '현재위치', 'send': 'ᏫᎦᏅᏗ', 'main': 'ᎠᎢᏎᏍᏗ', 'req': '요청값', 'hot': 'ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ', 'pump': 'ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'ᎤᏁᏤᎸᎩ', 'shell': 'ᎤᏯᏍᎦ', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'color': '색상', 'click': 'ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': '끝위치', 'command_mode': 'ᎤᏁᏤᎸᎩ_ᎬᏙᏗ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
