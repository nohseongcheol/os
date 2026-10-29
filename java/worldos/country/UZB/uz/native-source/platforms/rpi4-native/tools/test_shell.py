#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_koordinata', 'msg': 'Tarmoq_xabar', 'i': '순번', 'reply': 'javob_berish', 'call': '호출', 'args': 'dalil_ARRAY', 'chunk': '조각', 'data': 'ma_lumotlar', 'proc': 'Jarayon', 'long_text': '긴글', 'restored': '복원자료', 'send': 'yuborish', 'file': 'Fayl', 'main': 'Bajarish', 'found': 'Izlash_o_lchov', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'marker': '확인표시', 'command': 'Buyruq', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'qobiq', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'to_xtatmoq_OFFSET', 'image': 'rasm', 'key': '누름값', 'y': 'Y_tugmasi_koordinat', 'output': '출력결과', 'result': 'o_lchov', 'client': 'mijoz', 'line': 'satr', 'stream': 'oqim_VALUE', 'name': 'Nomi', 'value': 'VALUE', 'receive': '수신하기', 'report': 'tasdiq_hisobot', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
