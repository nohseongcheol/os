#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'kusu_pütchi', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': '실행하기', 'cancel': 'oo_ulawaa_akumajiraa', 'cmd_byte': 'aluwataaya_waai', 'reply': '응답', 'points': '지점들', 'server': '서버', 'data': 'atijaaya', 'prompt': 'a_atapajülü', 'enter': '들어가기', 'imported': '들여온파일', 'send': 'ajütaa', 'main': '시작', 'ROOT': '기준', 'text': '글', 'first_gui': '첫화면', 'pixel': 'pikserü', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'pikserü_anaajaalaa', 'pixels_data': 'pikserü_atijaaya', 'edit': 'anaataa_ajutuu', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': '크기', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'matchanta', 'line': 'liinia', 'report': 'anaajiaakua_ipa_achikiimaajatü', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'ashakatiraa', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': '실행과정', 'content': 'alu_ujatüü_ajutuu', 'block': '자료덩이', 'marker': '확인표시', 'command': 'aluwataaya', 'expected': '예상결과', 'shell': 'aluwataalapu_u', 'drawing': '그림경로', 'f': 'anaajaalaa_ekeroliaa', 'transcript': '대화기록', 'offset': '변위', 'path': 'wopu_a_ttaaleemüin', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'palantüsü_ajutuu', 'cmd': '명령인수', 'name': '이름', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
