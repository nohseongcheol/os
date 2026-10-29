#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/원격한글시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Գործարկել', 'profile': 'Հատկագիր', 'focused': 'Կարեւոր_գործարքներ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'սպասարկիչ_արժեք', 'log': 'մատյան_տող', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'deadline': '마감시각', 'data': 'տվյալ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Գործարկել', 'ready': '준비완료', 'found': 'որոնել_չափ', 'guest': 'հյուր', 'ROOT': 'արձակել_արմատ', 'marker': '확인표시', 'text': 'Տեքստ', 'out': 'չափ_տվյալ', 'env': '환경', 'f': 'նիշք_մուտքագրում', 'port': '접속번호', 'offset': 'Տեղաշարժում_արժեք', 'version': '판번호', 'p': 'տվյալ_դիրք', 'selector': 'ընտրիչ', 'xvfb': 'վիրտուալ_ցուցադրել', 'display': 'ցուցադրիչ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Անուն', 'window': 'պատուհան', 'report': 'վավերացում_զեկույց', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
