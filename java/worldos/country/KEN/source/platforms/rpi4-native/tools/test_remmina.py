#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/원격한글시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'endesha', 'profile': 'Maelezo_mafupi', 'focused': 'Lengwa', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'seva_thamani', 'log': 'batli_REKODI', 'args': 'hoja_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'endesha', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'mgeni', 'ROOT': '기준', 'marker': '확인표시', 'text': 'SMS', 'out': '결과자료', 'env': '환경', 'f': 'faili_ingizo', 'port': 'namba_ya_kituo', 'offset': 'Chipua_thamani', 'version': '판번호', 'p': '자료위치', 'selector': 'kiteuzi', 'xvfb': 'pepe_onyesha', 'display': 'uonyesho', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Jina', 'window': 'dirisha', 'report': 'uhakikishi_ripoti', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
