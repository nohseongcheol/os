#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/창시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'co_chomharra_x', 's': 'sreang_dàta', 'xy': 'càraid_àireimh', 'sel': 'roghnaichear_a916db4e', 'seconds': '초단위', 'log': 'LOG_ràgh', 'at': '현재위치', 'send': 'cuir', 'main': 'ruith', 'req': '요청값', 'hot': 'ath_ghoirid_VALUE', 'pump': 'làmhrachan_tachartas', 'ROOT': 'tilg_freumh', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'àithne', 'shell': 'slige', 'f': 'faidhle_cur_a_steach', 'color': '색상', 'click': 'briog_putan', 'k': '셋째순번', 'c': 'còd_a_charactair', 'r': '반환값', 'p': 'dàta_suidhich', 'done': '완료량', 'end': 'crìochnaich_OFFSET', 'command_mode': 'àithne_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'tomhas', 'report': 'dearbhadh_aithisg', 'dest': 'ceann_uidhe_VALUE_suidhich', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
