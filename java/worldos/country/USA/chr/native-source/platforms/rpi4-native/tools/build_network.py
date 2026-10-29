#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎪᏢᏍᎩ_ᏧᎾᏚᏓᎵ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎪᏢᏍᎩ_ᏧᎾᏚᏓᎵ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎪᏢᏍᎩ_ᏧᎾᏚᏓᎵ')
    대응 = {'obj': 'ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ', 'objects': '목적파일들', 'library': 'ᏧᏂᎪᎵᏰᏗᎢ', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ', 'source': '원본자료', 'run': 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', 'flags': '설정비트', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
