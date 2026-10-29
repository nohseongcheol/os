#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/셸시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'gamayyar_x', 'msg': 'Hanyar_sadarwa_imel', 'i': '순번', 'reply': 'mayar_da_martani', 'call': '호출', 'args': 'Tubalin_aiki_TSARI', 'chunk': '조각', 'data': 'Tarin_bayani', 'proc': 'haryar_aikin_na_ura', 'long_text': '긴글', 'restored': '복원자료', 'send': 'Aika', 'file': 'Fayil', 'main': 'Tafiyar_da', 'found': '찾은결과', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'command': 'Umarni', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'Mai_fayyace_umani', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'Ƙarshe_Sassautawa', 'image': 'Hoto', 'key': '누름값', 'y': 'Maɓallin_Y_Mai_tsarawa', 'output': '출력결과', 'result': '결과', 'client': 'abokin_hulda', 'line': 'Layi', 'stream': 'watsuwa_Daraja', 'name': 'Suna', 'value': 'Daraja', 'receive': '수신하기', 'report': 'amincewa_Rahoto', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
