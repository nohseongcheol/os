#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_koordinatı', 's': 'sətir_verilənlər', 'i': '순번', 'sel': 'seçici_a916db4e', 'seconds': '초단위', 'log': 'LOG_yaz', 'data': 'verilənlər', 'at': '현재위치', 'send': 'göndərmək', 'main': 'İcra_Et', 'req': 'HTTP_sorğusu_VALUE', 'hot': 'qısayol_VALUE', 'pump': 'tutacaq_hadisə', 'ROOT': 'Project_kök', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Əmr', 'shell': 'örtük', 'f': 'fayl_daxiletmə', 'click': 'klikləmə_düymə', 'k': '셋째순번', 'c': 'simvol_kodu', 'r': '반환값', 'p': 'verilənlər_yerinə_qoymaq', 'command_mode': 'əmr_MODE', 'end': 'bitirmək_OFFSET', 'classes': 'Sinif_yol', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'ölçü', 'report': 'yoxlama_hesabat', 'dest': 'təyinat_VALUE_yerinə_qoymaq', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
