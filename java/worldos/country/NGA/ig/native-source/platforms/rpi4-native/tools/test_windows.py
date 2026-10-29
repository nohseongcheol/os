#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/창시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'ngakọrịta_x', 's': 'ùsòròokwū_datà', 'xy': 'mkpị_nkwụgbà', 'sel': 'ihe_nhọpụta_a916db4e', 'seconds': '초단위', 'log': 'ndekọ_NDEKỌ', 'at': '현재위치', 'send': 'zìga', 'main': 'Bido', 'req': '요청값', 'hot': 'ụzọnsō_valuu', 'pump': 'ebenjìaka_mmèrème', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Ntiiwu', 'shell': 'nkọwannyemiwu', 'f': 'ọbọakwụkwọ_ndebà', 'color': '색상', 'click': 'pịkịnye_ọdụmbi', 'k': '셋째순번', 'c': 'koòdù_nkeakàrà', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'mèdebe_Nnokwata', 'command_mode': 'nnyemiwu_moòdù', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'nkwèputaonòdù_akụkọ', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
