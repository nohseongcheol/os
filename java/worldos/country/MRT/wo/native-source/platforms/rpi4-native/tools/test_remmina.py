#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/원격한글시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'daw', 'profile': 'profil', 'focused': 'Yiñ_fësal', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'dëggu_xëyma', 'log': 'làq_Dënk', 'args': 'Tegtal_TABLO', 'deadline': '마감시각', 'data': 'mbir', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'daw', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'gan', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Tekst', 'out': '결과자료', 'env': '환경', 'f': 'bara_denc_dugal_xabaar', 'port': '접속번호', 'offset': 'Randal_xëyma', 'version': '판번호', 'p': '자료위치', 'selector': 'tànnkat', 'xvfb': 'luy_feeñ_te_jëmmadi_laa', 'display': 'laa', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'tur_253d1510', 'window': 'palanteer', 'report': 'wéral_tënk', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
