#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/예제시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'տվյալ', 'graphics_command': 'պատկերանյութ_հրաման', 'main': 'Գործարկել', 'row': 'տող_դիրք', 'init': '초기값', 'target': 'թիրախ', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'binary': 'երկուական', 'out': 'չափ_տվյալ', 'entry': 'մուտքագրում_կետ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Մեկնարկ_նկար', 'col': 'սյունակ_դիրք', 'begin': 'Մեկնարկ_Տեղաշարժում', 'kind': 'անվանակարգ_արժեք', 'selector': 'ընտրիչ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'սպասառու', 'line': 'կապ', 'report': 'վավերացում_զեկույց', 'language': 'Լեզու', 'x': 'x_կոորդինատ', 'start': 'Գործարկել', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ուղարկել_Ցուցակ', 'payload': 'օգտակար_բեռնվածք_տվյալ', 'proc': 'Գործընթաց', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'անուն_աղյուսակ', 'content': 'Բովանդակություն_արժեք', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'նիշք_մուտքագրում_անուն', 'shell': 'խեցի', 'color': '색상', 'transcript': '대화기록', 'offset': 'Տեղաշարժում_արժեք', 'h': '높이값', 'run': 'կատարել_հրաման', 'c': 'գրանշանի_կոդ', 'path': 'Ճանապարհ', 'encoding': 'գրանշանների_կազմ', 'end': 'վերջացնել_Տեղաշարժում', 'ftp': 'նիշք_փոխանցել_կապ', 'pixels': '화소들', 'symbol': 'նշան_արժեք', 'source': '원본자료', 'name': 'Անուն', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
