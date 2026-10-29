#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/ડેસ્કટૉપ_જુઓ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('ડેસ્કટૉપ_જુઓ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ડેસ્કટૉપ_જુઓ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ભૂલ', 'exact': '정확한값', 'network': 'નેટવર્ક', 'closed': '닫힘', 'length': 'લંબાઈ_મૂલ્ય', 'opened': '열림', 'ftp_port': 'ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર', 'server': 'સર્વર_મૂલ્ય', 'resources': 'સાધનો', 'data': 'ડેટા', 'shift': 'SHIFT_કી', 'send': 'મોકલો', 'run_desktop': 'ચલાવો_ડેસ્કટૉપ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'હોસ્ટ', 'text': 'લખાણ', 'korean': '한글여부', 'port': 'પોર્ટ_નંબર', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'બ્રિજ', 'kind': 'શ્રેણી_મૂલ્ય', 'tail': '끝부분', 'size': 'માપ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ક્લાયંટ', 'char': 'વર્ણ_ડેટા', 'work': '작업경로', 'Keyboard': 'કીબોર્ડ', 'x': 'x_યામ', 'down': '누르는중', 'net': 'નેટવર્ક_બ્રિજ_પ્રવેશ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'દલીલ_અરે', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'પ્રક્રિયા', 'Desktop': 'કનેક્ટ_ડેસ્કટૉપ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'સ્વિચ_મોડ', 'command': 'આદેશ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_કી', 'path': 'પથ', 'cp': 'વર્ણ_એન્કોડિંગ', 'terminate': '종료시키기', 'security': 'સુરક્ષા', 'vnc_port': '원격화면접속번호', 'body': 'મુખ્ય_પાઠ', 'index': 'લુકઅપ_અનુક્રમણિકા', 'exited': '종료됨', 'keysym': 'કી_પ્રતીક', 'output': '출력결과', 'keyboard': 'કીબોર્ડ_પ્રવેશ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'રીડર', 'NetworkBridge': 'નેટવર્ક_બ્રિજ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
