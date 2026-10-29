#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ᎠᏍᏘ_ᎦᏟᏌᏅᎯ', 'actual': '실제결과', 'match': '일치', 'payload': 'ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ', 'cases': 'ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ', 'fixture': 'ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏟᏌᏅᎯ', 'main': 'ᎠᎢᏎᏍᏗ', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'ᏚᏙᎥᎢ', 'jar': '자바꾸러미', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'tests': 'ᎠᏓᎪᎵᏰᏍᎩ_ᏕᎦᏅᏅᏛ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
