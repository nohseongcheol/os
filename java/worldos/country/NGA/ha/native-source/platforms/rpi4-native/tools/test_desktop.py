#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/바탕화면시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'gamayyar_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Tafiyar_da', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'alama_ad6f1a96', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'haryar_aikin_na_ura', 'data': 'Tarin_bayani', 'main': 'Tafiyar_da', 'w': '너비값', 'init': '초기값', 'block': 'Tarin_bayani_bulo', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'report': 'amincewa_Rahoto', 'until': '까지', 'clipboard': 'Allon_zane_Daraja', 'dst': 'Zangon_ƙarshe_imel', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'lambar_kafa', 'offset': 'Sassautawa_Daraja', 'h': '높이값', 'src': '원본주소', 'event': 'Faruwa', 'encoding': 'Ƙunshin_alƙalumma', 'size': 'Girma', 'key': '누름값', 'pixels': '화소들', 'y': 'Maɓallin_Y_Mai_tsarawa', 'output': '출력결과', 'symbol': 'alama_Daraja', 'client': 'abokin_hulda', 'char': 'Harafi_Tarin_bayani', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
