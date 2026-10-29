#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/원격한글시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'dirisa', 'profile': 'Porofaele', 'focused': 'Tlhomameng', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'sefara_Boleng', 'log': 'rekota_mola', 'args': 'Thulaganyo_setlhopha', 'deadline': '마감시각', 'data': 'tshedimosetso', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'dirisa', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'moeng', 'ROOT': '기준', 'marker': '확인표시', 'text': 'SMS', 'out': '결과자료', 'env': '환경', 'f': 'faele_tsenyo', 'port': '접속번호', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'version': '판번호', 'p': '자료위치', 'selector': 'setlhophi', 'xvfb': 'seka_bontsha', 'display': 'sebontshi', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'leina', 'window': 'fensetere', 'report': 'netefatso_pego', 'work': '작업경로'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
