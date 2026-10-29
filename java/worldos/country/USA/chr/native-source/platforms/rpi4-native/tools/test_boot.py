#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ', 'cancel': 'ᎠᏎᏒᏗ_ᎠᎢᏒᎢ', 'cmd_byte': 'ᎤᏁᏤᎸᎩ_byte', 'reply': '응답', 'points': '지점들', 'server': 'ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ', 'data': 'ᎦᏟᏌᏅᎯ', 'prompt': 'ᎦᏅᏫᏍᏗᏍᎩ', 'enter': 'ᎥᎧᏁᏉᏍᎬᎢ', 'imported': '들여온파일', 'send': 'ᏫᎦᏅᏗ', 'main': 'ᎠᎢᏎᏍᏗ', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'pel_ᎠᏍᏆᏂᎪᏙᏗ', 'pixels_data': 'pel_ᎦᏟᏌᏅᎯ', 'edit': 'ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ', 'receive_until': '표시까지받기', 'selector': 'ᎠᏑᏰᏍᎩ', 'size': 'ᎢᎩᏓ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'ᎠᏥᏍᏕᎵᏍᎩ', 'line': 'ᏚᏓᏅᏅᎢ', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'content': 'ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ', 'block': 'ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ', 'marker': '확인표시', 'command': 'ᎤᏁᏤᎸᎩ', 'expected': '예상결과', 'shell': 'ᎤᏯᏍᎦ', 'drawing': 'ᎠᏍᏓᏅᎿᏂᏙᎸ_ᎠᏍᏓᏩᏛᏍᏗ', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'transcript': '대화기록', 'offset': '변위', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ', 'cmd': '명령인수', 'name': 'ᏚᏙᎥᎢ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
