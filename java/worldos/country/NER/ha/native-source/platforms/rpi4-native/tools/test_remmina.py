#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/원격한글시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Tafiyar_da', 'profile': 'furofayil', 'focused': 'Muhimmi', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'Saba_Daraja', 'log': 'logu_naɗa', 'args': 'Tubalin_aiki_TSARI', 'deadline': '마감시각', 'data': 'Tarin_bayani', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Tafiyar_da', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'baƙo', 'ROOT': '기준', 'marker': '확인표시', 'text': 'SMS', 'out': '결과자료', 'env': '환경', 'f': 'Fayil_Mashigar_bayanai', 'port': 'lambar_kafa', 'offset': 'Sassautawa_Daraja', 'version': '판번호', 'p': '자료위치', 'selector': 'mai_zabe', 'xvfb': 'Mai_alaka_da_aikin_na_ura_na_boye_Nuna', 'display': 'Nuna', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Suna', 'window': 'taga', 'report': 'amincewa_Rahoto', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
