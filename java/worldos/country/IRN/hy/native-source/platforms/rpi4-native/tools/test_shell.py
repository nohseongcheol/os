#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/셸시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_կոորդինատ', 'msg': 'Ցանց_ուղերձ', 'i': '순번', 'reply': 'պատասխանել', 'call': '호출', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'chunk': '조각', 'data': 'տվյալ', 'proc': 'Գործընթաց', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ուղարկել', 'file': 'Ֆայլ', 'main': 'Գործարկել', 'found': 'որոնել_չափ', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'marker': '확인표시', 'command': 'Հրահանգ', 'expected': '예상결과', 'pixel': 'փիքսել', 'shell': 'խեցի', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'վերջացնել_Տեղաշարժում', 'image': 'նկար', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'չափ', 'client': 'սպասառու', 'line': 'կապ', 'stream': 'հոսք_արժեք', 'name': 'Անուն', 'value': 'արժեք', 'receive': '수신하기', 'report': 'վավերացում_զեկույց', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
