#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 진입점. 실제 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as ПУТАЊА
체계.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': '통신문', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Изврши', 'cancel': '취소', 'cmd_byte': '명령바이트', 'reply': '응답', 'points': '지점들', 'server': '서버', 'data': '자료', 'prompt': '안내문', 'enter': '들어가기', 'imported': '들여온파일', 'send': '보내기', 'main': 'Покрени', 'ROOT': '기준', 'text': 'Текст', 'first_gui': '첫화면', 'pixel': '화소', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': '화소파일', 'pixels_data': '화소자료', 'edit': '편집', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'Величина', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ИСХОД', 'samples': '예제들', 'client': '접속자', 'line': 'Ред', 'report': '검증기록', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': '내려받기', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Процес', 'content': '내용', 'block': '자료덩이', 'marker': '확인표시', 'command': 'Наредба', 'expected': '예상결과', 'shell': '셸', 'drawing': '그림경로', 'f': '파일항목', 'transcript': '대화기록', 'offset': '변위', 'path': 'ПУТАЊА', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': '흐름', 'cmd': '명령인수', 'name': 'Назив', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
