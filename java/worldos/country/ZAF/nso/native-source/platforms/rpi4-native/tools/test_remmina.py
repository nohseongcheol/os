#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/원격한글시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Diriša', 'profile': 'Profaele', 'focused': 'Šeditše', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'seba_boleng', 'log': 'pego_rei', 'args': 'akumente_arei', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Diriša', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'moeng', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Sengwalwa', 'out': '결과자료', 'env': '환경', 'f': 'faele_go_tsenya_tshedimošo', 'port': '접속번호', 'offset': 'E_Šetšego_boleng', 'version': '판번호', 'p': '자료위치', 'selector': 'sekgethi', 'xvfb': 'sethalwa_bontšha', 'display': 'sebontšhi', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Leina', 'window': 'lefastere', 'report': 'tiišetšo_pego', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
