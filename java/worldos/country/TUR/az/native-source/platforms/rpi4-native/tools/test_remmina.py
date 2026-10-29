#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'İcra_Et', 'profile': 'Profil', 'focused': 'Fokuslanmış', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_yaz', 'args': 'arqument_ARRAY', 'deadline': '마감시각', 'data': 'verilənlər', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'İcra_Et', 'ready': '준비완료', 'found': 'SEARCH_ölçü', 'guest': 'qonaq', 'ROOT': 'Project_kök', 'marker': '확인표시', 'text': 'Mətn', 'out': 'ölçü_verilənlər', 'env': '환경', 'f': 'fayl_daxiletmə', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': 'versiya_nömrəsi', 'p': 'verilənlər_yerinə_qoymaq', 'selector': 'seçici', 'xvfb': 'virtual_displey', 'display': 'displey', 'n': 'element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ad', 'window': 'pəncərə', 'report': 'yoxlama_hesabat', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
