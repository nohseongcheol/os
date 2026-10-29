#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/화면요소시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'gamayyar_x', 's': 'Zare_Tarin_bayani', 'i': '순번', 'sel': 'mai_zabe_a916db4e', 'seconds': '초단위', 'log': 'logu_naɗa', 'data': 'Tarin_bayani', 'at': '현재위치', 'send': 'Aika', 'main': 'Tafiyar_da', 'req': '요청값', 'hot': 'Hada_lambobi_Daraja', 'pump': 'Mariki_Faruwa', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Umarni', 'shell': 'Mai_fayyace_umani', 'f': 'Fayil_Mashigar_bayanai', 'click': 'Danna_maɓali', 'k': '셋째순번', 'c': 'Lambar_sirrin_harafi', 'r': '반환값', 'p': '자료위치', 'command_mode': 'Umarni_yanayin_aiki', 'end': 'Ƙarshe_Sassautawa', 'classes': 'Aji_Hanyar_shiga', 'key': '누름값', 'y': 'Maɓallin_Y_Mai_tsarawa', 'result': '결과', 'report': 'amincewa_Rahoto', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
