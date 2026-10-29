#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/원격한글시험.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ᎠᎢᏎᏍᏗ', 'profile': 'ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ', 'focused': '초점요소', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ', 'log': 'ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'deadline': '마감시각', 'data': 'ᎦᏟᏌᏅᎯ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ᎠᎢᏎᏍᏗ', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'ᎠᏓᏩᏛᎯᏙᎯ', 'ROOT': '기준', 'marker': '확인표시', 'text': 'ᎠᎪᎵᏰᏗ', 'out': '결과자료', 'env': '환경', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'port': '접속번호', 'offset': '변위', 'version': '판번호', 'p': '자료위치', 'selector': 'ᎠᏑᏰᏍᎩ', 'xvfb': 'ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎬᏂᎨᏒ_ᏅᎦ', 'display': 'ᎬᏂᎨᏒ_ᏱᎬᏁᏗᎢ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ᏚᏙᎥᎢ', 'window': 'ᏦᎳᏂ', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
