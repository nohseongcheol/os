#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/창시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'jira_x', 's': 'tungo_data', 'xy': 'Jozi_ratibu', 'sel': 'kiteuzi_a916db4e', 'seconds': '초단위', 'log': 'batli_REKODI', 'at': '현재위치', 'send': 'tuma', 'main': 'endesha', 'req': '요청값', 'hot': 'njia_ya_mkato_thamani', 'pump': 'kishiko_tukio', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'amri', 'shell': 'sheli', 'f': 'faili_ingizo', 'color': '색상', 'click': 'bofya_kitufe', 'k': '셋째순번', 'c': 'msimbo_wa_kibambo', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'tamatia_Chipua', 'command_mode': 'amri_hali_tumizi', 'key': '누름값', 'y': 'Kitufe_cha_Y_kiratibu', 'pixels': '화소들', 'result': '결과', 'report': 'uhakikishi_ripoti', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
