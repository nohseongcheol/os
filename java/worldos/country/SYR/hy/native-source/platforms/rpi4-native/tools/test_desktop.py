#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/바탕화면시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_կոորդինատ', 'typing': '글자입력', 'message': '알림문', 'start': 'Գործարկել', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'նշան', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Գործընթաց', 'data': 'տվյալ', 'main': 'Գործարկել', 'w': '너비값', 'init': '초기값', 'block': 'տվյալ_արգելափակել', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'marker': '확인표시', 'report': 'վավերացում_զեկույց', 'until': '까지', 'clipboard': 'սեղմատախտակ_արժեք', 'dst': 'նպատակակետ_հասցե', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Տեղաշարժում_արժեք', 'h': '높이값', 'src': '원본주소', 'event': 'միջոցառում', 'encoding': 'գրանշանների_կազմ', 'size': 'Չափս', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'նշան_արժեք', 'client': 'սպասառու', 'char': 'գրանշան_տվյալ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
