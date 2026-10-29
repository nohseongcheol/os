#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/원격한글시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ihuriro', 'profile': 'Umwirondoro', 'focused': 'Kihariye', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'seriveri_agaciro', 'log': 'kubika_umurongo', 'args': 'ingingo_ARRAY', 'deadline': '마감시각', 'data': 'amakurushingiro', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ihuriro', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Umwandiko', 'out': '결과자료', 'env': '환경', 'f': 'dosiye_icyinjizwa', 'port': '접속번호', 'offset': 'Ofuseti_agaciro', 'version': '판번호', 'p': '자료위치', 'selector': 'muhitamo', 'xvfb': 'kidafatika_kwerekana', 'display': 'kwerekana', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Izina', 'window': 'idirishya', 'report': 'iyemeza_raporo', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
