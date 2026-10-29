#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/셸시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_koordinatı', 'msg': 'Şəbəkə_mesaj', 'i': '순번', 'reply': 'cavab', 'call': '호출', 'args': 'arqument_ARRAY', 'chunk': '조각', 'data': 'verilənlər', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'göndərmək', 'file': 'FAYL', 'main': 'İcra_Et', 'found': 'SEARCH_ölçü', 'ROOT': 'Project_kök', 'text': 'Mətn', 'marker': '확인표시', 'command': 'Əmr', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'örtük', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'bitirmək_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_koordinat', 'output': '출력결과', 'result': 'ölçü', 'client': 'müştəri', 'line': 'Giriş', 'stream': 'axın_VALUE', 'name': 'Ad', 'value': 'VALUE', 'receive': '수신하기', 'report': 'yoxlama_hesabat', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
