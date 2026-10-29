#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_koordinata', 's': 'satr_ma_lumotlar', 'i': '순번', 'sel': 'tanlagich_a916db4e', 'seconds': '초단위', 'log': 'LOG_satr', 'data': 'ma_lumotlar', 'at': '현재위치', 'send': 'yuborish', 'main': 'Bajarish', 'req': '요청값', 'hot': 'yorliq_VALUE', 'pump': 'deskriptor_hodisa', 'ROOT': 'Project_ildiz', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Buyruq', 'shell': 'qobiq', 'f': 'fayl_kiritish', 'click': 'chertmoq_tugma', 'k': '셋째순번', 'c': 'belgi_kodi', 'r': '반환값', 'p': 'ma_lumotlar_holat', 'command_mode': 'buyruq_MODE', 'end': 'to_xtatmoq_OFFSET', 'classes': 'Sinf_yo_l', 'key': '누름값', 'y': 'Y_tugmasi_koordinat', 'result': 'o_lchov', 'report': 'tasdiq_hisobot', 'dest': 'ko_chirish_joyi_VALUE_holat', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
