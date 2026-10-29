#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    vastendamine_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Käivita_2', 'profile': 'Profiil', 'focused': 'Fookuses', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_kirje', 'args': 'argument_ARRAY', 'deadline': 'tähtaeg_Aeg', 'data': 'andmed', 'candidate': '후보', 'logs': '기록들', 'kw': 'nimeline_argument', 'number': '수치', 'main': 'Käivita_2', 'ready': '준비완료', 'found': 'Otsi_näitaja', 'guest': 'külaline', 'ROOT': 'Project_juur', 'marker': 'marker', 'text': 'Tekst', 'out': 'näitaja_andmed', 'env': '환경', 'f': 'Fail_kirje', 'port': 'pordinumber', 'offset': 'nihe_VALUE', 'version': 'versiooninumber', 'p': 'andmed_ametikoht', 'selector': 'valija', 'xvfb': '가상표시장치', 'display': 'ekraan', 'n': 'kaup_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nimi_2', 'window': 'aken', 'report': 'kinnitamine_aruanne', 'work': '작업경로'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
