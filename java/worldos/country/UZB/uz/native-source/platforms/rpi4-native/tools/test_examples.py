#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'kiritish_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ma_lumotlar', 'graphics_command': 'grafika_buyruq', 'main': 'Bajarish', 'row': 'ROW_holat', 'init': '초기값', 'target': 'nishon', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'binary': 'binar', 'out': 'o_lchov_ma_lumotlar', 'entry': 'kiritish_nuqta', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_chizish', 'col': 'ustun_holat', 'begin': 'Start_OFFSET', 'kind': 'toifa_VALUE', 'selector': 'tanlagich', 'n': 'element_COUNT', 'key': '누름값', 'y': 'Y_tugmasi_koordinat', 'client': 'mijoz', 'line': 'satr', 'report': 'tasdiq_hisobot', 'language': 'Til', 'x': 'x_koordinata', 'start': 'Bajarish', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'yuborish_Ro_yxat', 'payload': 'foydali_yuklanma_ma_lumotlar', 'proc': 'Jarayon', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'nom_jadval', 'content': 'tarkib_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fayl_kiritish_nom', 'shell': 'qobiq', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'bajarmoq_buyruq', 'c': 'belgi_kodi', 'path': 'yo_l', 'encoding': 'belgilar_to_plami', 'end': 'to_xtatmoq_OFFSET', 'ftp': 'fayl_uzatish_aloqa', 'pixels': '화소들', 'symbol': 'ramz_VALUE', 'source': '원본자료', 'name': 'Nomi', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
