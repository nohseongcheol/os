#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Bajarish', 'profile': 'Profil', 'focused': 'Muhim', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_satr', 'args': 'dalil_ARRAY', 'deadline': '마감시각', 'data': 'ma_lumotlar', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Bajarish', 'ready': '준비완료', 'found': 'Izlash_o_lchov', 'guest': 'mehmon', 'ROOT': 'Project_ildiz', 'marker': '확인표시', 'text': 'Matn', 'out': 'o_lchov_ma_lumotlar', 'env': '환경', 'f': 'fayl_kiritish', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'ma_lumotlar_holat', 'selector': 'tanlagich', 'xvfb': 'virtual_ekran', 'display': 'ekran', 'n': 'element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nomi', 'window': 'oyna', 'report': 'tasdiq_hisobot', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
