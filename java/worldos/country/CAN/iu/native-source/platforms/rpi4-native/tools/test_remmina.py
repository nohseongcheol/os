#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/원격한글시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': '시작', 'profile': 'Miksaanuungajuq', 'focused': '초점요소', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ikiaqqitittivik_atuutilik', 'log': 'papattivik_sanimukutaak', 'args': 'aturniqarnirainiq_array', 'deadline': '마감시각', 'data': 'titiqqat', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': '시작', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'titiqqaq', 'out': '결과자료', 'env': '환경', 'f': 'ini_Iliniku', 'port': '접속번호', 'offset': '변위', 'version': '판번호', 'p': '자료위치', 'selector': '준비선택기', 'xvfb': 'saqqijaanganngittuq_saqqijaarli', 'display': 'saqqijaarli', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'atiq', 'window': 'igalaangujaq', 'report': 'naammannirainiq_unikkaaq', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
