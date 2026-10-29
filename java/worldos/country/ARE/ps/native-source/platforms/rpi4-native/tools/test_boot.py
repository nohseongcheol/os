#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'جال_استوزه', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'چلول', 'cancel': 'ړنګونه_چلښت', 'cmd_byte': 'بولۍ_بايټ', 'reply': '응답', 'points': '지점들', 'server': '서버', 'data': 'اومتوک', 'prompt': 'پارليکه', 'enter': '들어가기', 'imported': '들여온파일', 'send': 'استول', 'main': 'ځغلول', 'ROOT': '기준', 'text': 'ليکنه', 'first_gui': '첫화면', 'pixel': 'پکسل', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'پکسل_دوتنه', 'pixels_data': 'پکسل_اومتوک', 'edit': 'سمون_ارزښت', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'کچ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'پېرن', 'line': 'ليکه', 'report': 'باورکړن_راپور', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'رالېښل', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'بهير', 'content': 'منځپانګه_ارزښت', 'block': '자료덩이', 'marker': '확인표시', 'command': 'بولۍ', 'expected': '예상결과', 'shell': 'سیپۍ', 'drawing': '그림경로', 'f': 'دوتنه_ننوت', 'transcript': '대화기록', 'offset': '변위', 'path': 'يونلور', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'بهنګ_ارزښت', 'cmd': '명령인수', 'name': 'نوم', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
