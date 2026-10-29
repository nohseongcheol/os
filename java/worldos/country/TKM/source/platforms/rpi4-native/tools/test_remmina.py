#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/원격한글시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Bitir', 'profile': 'profil', 'focused': 'Fokusly', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'serwer_baha', 'log': 'hasaba_alyş_setir', 'args': 'argument_ARRAY', 'deadline': '마감시각', 'data': 'maglumat', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Bitir', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Metin', 'out': '결과자료', 'env': '환경', 'f': 'faýl_girizmeklik', 'port': '접속번호', 'offset': 'Süýşüriş_baha', 'version': '판번호', 'p': '자료위치', 'selector': 'saýlaýjy', 'xvfb': 'hyýaly_ekran', 'display': 'ekran', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ad', 'window': 'penjire', 'report': 'barlag_hasabat', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
