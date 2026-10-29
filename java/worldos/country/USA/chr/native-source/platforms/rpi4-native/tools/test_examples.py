#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/예제시험.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ᎦᏟᏌᏅᎯ', 'graphics_command': '그림명령', 'main': 'ᎠᎢᏎᏍᏗ', 'row': '행위치', 'init': '초기값', 'target': 'ᎠᏉᏅᏗᎢ', 'ROOT': '기준', 'text': 'ᎠᎪᎵᏰᏗ', 'binary': 'binary', 'out': '결과자료', 'entry': 'Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'ᎭᏂᎩᏍᏓ_ᎠᏍᏓᏅᎿᏂᏙᎸ', 'col': '열위치', 'begin': '시작위치', 'kind': 'ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ', 'selector': 'ᎠᏑᏰᏍᎩ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ᎠᏥᏍᏕᎵᏍᎩ', 'line': 'ᏚᏓᏅᏅᎢ', 'report': 'ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ', 'language': 'ᎦᏬᏂᎯᏍᏗ', 'x': '가로좌표', 'start': 'ᎠᎢᏎᏍᏗ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ᏫᎦᏅᏗ_ᏕᎦᏅᏅᏛ', 'payload': 'ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ', 'proc': 'ᎢᏯᏛᏁᎵᏓᏍᏗ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ', 'content': 'ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏬᏂᎯᏍᏗ', 'filename': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ', 'shell': 'ᎤᏯᏍᎦ', 'color': '색상', 'transcript': '대화기록', 'offset': '변위', 'h': '높이값', 'run': 'ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', 'c': '문자값', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'encoding': 'ᎪᏪᎸ_ᎤᎾᏓᏡᎬ', 'end': '끝위치', 'ftp': 'ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ', 'pixels': '화소들', 'symbol': '심볼', 'source': '원본자료', 'name': 'ᏚᏙᎥᎢ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
