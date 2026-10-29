#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ruith', 'profile': 'Pròifil', 'focused': 'fòcasaichte', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'frithealaiche_VALUE', 'log': 'LOG_ràgh', 'args': 'argamaid_ARRAY', 'deadline': '마감시각', 'data': 'dàta', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ruith', 'ready': '준비완료', 'found': 'lorg_tomhas', 'guest': 'aoigh', 'ROOT': 'tilg_freumh', 'marker': '확인표시', 'text': 'SMS', 'out': 'tomhas_dàta', 'env': '환경', 'f': 'faidhle_cur_a_steach', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'dàta_suidhich', 'selector': 'roghnaichear', 'xvfb': 'mas_fhìor_taisbean', 'display': 'uidheam_taisbeanaidh', 'n': 'nì_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ainm', 'window': 'uinneag', 'report': 'dearbhadh_aithisg', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
