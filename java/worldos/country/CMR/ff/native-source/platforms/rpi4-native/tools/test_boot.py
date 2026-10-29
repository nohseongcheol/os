#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'laylaytol_ɓatakuru', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': '실행하기', 'cancel': 'haaytude_hiisoore', 'cmd_byte': 'ginol_oktee', 'reply': '응답', 'points': '지점들', 'server': 'sarworde_njaru', 'data': 'keɓe', 'prompt': 'hirjinaango', 'enter': 'naatnude', 'imported': '들여온파일', 'send': 'neldude', 'main': 'huutoraade', 'ROOT': '기준', 'text': 'binndi', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'piksel_fiilde', 'pixels_data': 'piksel_keɓe', 'edit': 'feewnditde_njaru', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'waylude_etannde', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'kiliyaan', 'line': 'diidol', 'report': 'teeŋtingol_ciimtol', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'loowtude', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Yuɓɓo_golle', 'content': 'loowdi_njaru', 'block': '자료덩이', 'marker': '확인표시', 'command': 'ginol', 'expected': '예상결과', 'shell': 'laalagal', 'drawing': 'natal_laawol', 'f': 'fiilde_naatnugol', 'transcript': '대화기록', 'offset': '변위', 'path': 'laawol', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'waraango_njaru', 'cmd': '명령인수', 'name': 'innde', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
