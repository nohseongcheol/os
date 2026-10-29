#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/셸시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'جال_استوزه', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': 'ارزښتوړى_لړوند', 'chunk': '조각', 'data': 'اومتوک', 'proc': 'بهير', 'long_text': '긴글', 'restored': '복원자료', 'send': 'استول', 'file': 'دوتنه', 'main': 'ځغلول', 'found': '찾은결과', 'ROOT': '기준', 'text': 'ليکنه', 'marker': '확인표시', 'command': 'بولۍ', 'expected': '예상결과', 'pixel': 'پکسل', 'shell': 'سیپۍ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': 'انځور', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'پېرن', 'line': 'ليکه', 'stream': 'بهنګ_ارزښت', 'name': 'نوم', 'value': 'ارزښت', 'receive': '수신하기', 'report': 'باورکړن_راپور', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
