#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/화면요소시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'rëddu_iks_yi', 's': 'araf_yu_bennoo_mbir', 'i': '순번', 'sel': 'tànnkat_a916db4e', 'seconds': '초단위', 'log': 'làq_Dënk', 'data': 'mbir', 'at': '현재위치', 'send': 'Yónnee', 'main': 'daw', 'req': '요청값', 'hot': 'Teggi_xëyma', 'pump': 'yombal_xewxew', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'ndigel', 'shell': 'Wëreef', 'f': 'bara_denc_dugal_xabaar', 'click': 'bës_butoñ', 'k': '셋째순번', 'c': 'kotu_araf', 'r': '반환값', 'p': '자료위치', 'command_mode': 'ndigel_anam', 'end': 'jeexal_Randal', 'classes': 'maas_Yoonu_jëmale', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'wéral_tënk', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
