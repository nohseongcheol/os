#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/원격한글시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Bido', 'profile': 'Profaịl', 'focused': 'Mgbadoanya_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'savà_valuu', 'log': 'ndekọ_NDEKỌ', 'args': 'agụment_MKPOKỌTA', 'deadline': '마감시각', 'data': 'datà', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Bido', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'SMS', 'out': '결과자료', 'env': '환경', 'f': 'ọbọakwụkwọ_ndebà', 'port': '접속번호', 'offset': 'Nnokwata_valuu', 'version': '판번호', 'p': '자료위치', 'selector': 'ihe_nhọpụta', 'xvfb': 'kendìnuchè_gosịpụta', 'display': 'ngosịpụta', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Aha', 'window': 'windò', 'report': 'nkwèputaonòdù_akụkọ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
