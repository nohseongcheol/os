#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎪᏢᏍᎩ_ᎬᏗᏍᎩ_SPACE.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎪᏢᏍᎩ_ᎬᏗᏍᎩ_SPACE', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎪᏢᏍᎩ_ᎬᏗᏍᎩ_SPACE')
    대응 = {'mode': 'method_ᎬᏙᏗ', 'header': 'ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ', 'posix': '포직스경로', 'payload': 'ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ', 'flags': '설정비트', 'cases': 'ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ', 'cc': '시언어번역기', 'data': 'ᎦᏟᏌᏅᎯ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ᎠᎪᎵᏰᏗ', 'headers': 'ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏕᎦᏅᏅᏛ', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ᎪᏢᏍᎩ', 'build_users': '사용자영역만들기', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': '프로그램머리변위', 'offset': '변위', 'text_address': 'ᎤᏁᏤᎸᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ᏕᎦᎧᎲᎢ_ᏧᎬᏩᎶᏗᏯ', 'index': '색인', 'classes': 'ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ', 'symbol': '심볼', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ᏚᏙᎥᎢ', 'value': 'ᏧᎬᏩᎶᏗᏯ', 'fmt': 'ᏱᎬᏁᎸᎯ_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
