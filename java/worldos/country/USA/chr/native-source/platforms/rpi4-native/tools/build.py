#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ')
    대응 = {'network': 'ᏧᎾᏚᏓᎵ', 'BUILD': 'ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ', 'ar': 'ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎦᏟᏌᏅᎯ', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'method_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'main': 'ᎠᎢᏎᏍᏗ', 'objcopy': 'ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏁᏟᏴᏍᎩ', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'extra': '추가영역', 'exports': 'ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ', 'jobs': '빌드작업', 'run': 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'REPO': '저장소', 'tool': '도구', 'classes': 'ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': 'ᏚᏙᎥᎢ', 'build_network': '통신망만들기', 'font_info': 'ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎧᏃᎮᏢᎥᏍᎩ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
