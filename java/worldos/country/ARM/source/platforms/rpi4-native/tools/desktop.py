#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/սեղան_տեսք.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('սեղան_տեսք', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('սեղան_տեսք')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Սխալ', 'exact': '정확한값', 'network': 'Ցանց', 'closed': '닫힘', 'length': 'տեւողություն_արժեք', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'սպասարկիչ_արժեք', 'resources': 'Միջոցներ', 'data': 'տվյալ', 'shift': 'SHIFT_ստեղն', 'send': 'ուղարկել', 'run_desktop': 'աշխատեցնել_սեղան', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'հոստ', 'text': 'Տեքստ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'կամուրջ', 'kind': 'անվանակարգ_արժեք', 'tail': '끝부분', 'size': 'Չափս', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'սպասառու', 'char': 'գրանշան_տվյալ', 'work': '작업경로', 'Keyboard': 'ստեղնաշար', 'x': 'x_կոորդինատ', 'down': '누르는중', 'net': 'Ցանց_կամուրջ_մուտքագրում', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Գործընթաց', 'Desktop': 'Կապակցել_սեղան', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'փոխարկել_կերպ', 'command': 'Հրահանգ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_ստեղն', 'path': 'Ճանապարհ', 'cp': 'գրանշան_կոդավորում', 'terminate': '종료시키기', 'security': 'Անվտանգություն', 'vnc_port': '원격화면접속번호', 'body': 'հիմնական_գրվածք', 'index': 'Փնտրում_դասիչ', 'exited': '종료됨', 'keysym': 'ստեղն_նշան', 'output': '출력결과', 'keyboard': 'ստեղնաշար_մուտքագրում', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Ընթերցիչ', 'NetworkBridge': 'Ցանց_կամուրջ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
