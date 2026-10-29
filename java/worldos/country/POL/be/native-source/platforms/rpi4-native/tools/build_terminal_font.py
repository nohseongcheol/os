#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'дадзеныя', 'img': 'рукапісная_графіка_значэнне', 'bits': 'Служба_інтэлектуальнай_фонавай_перадачы_файлаў_Спіс', 'x': 'каардыната_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'шлях_Спіс', 'y': '세로좌표', 'main': 'Выканаць', 'src': '원본주소', 'fonts': 'шрыфт_Спіс', 'ROOT': '기준', 'p': '자료위치', 'cp': 'сімвал_кадаванне', 'target': 'мэтавы_паказчык'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
