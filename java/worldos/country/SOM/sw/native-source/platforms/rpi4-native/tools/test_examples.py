#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/예제시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'faili_hamisha_namba_ya_kituo', 'data': 'data', 'graphics_command': '그림명령', 'main': 'endesha', 'row': '행위치', 'init': '초기값', 'target': 'lengo', 'ROOT': '기준', 'text': 'SMS', 'binary': 'jozi', 'out': '결과자료', 'entry': 'ingizo_pointi', 'got': '받은수', 'port': 'namba_ya_kituo', 'graphics_start': 'Anza_mchoro', 'col': '열위치', 'begin': 'Anza_Chipua', 'kind': 'kategoria_thamani', 'selector': 'kiteuzi', 'n': '개수', 'key': '누름값', 'y': 'Kitufe_cha_Y_kiratibu', 'client': 'teja', 'line': 'laini', 'report': 'uhakikishi_ripoti', 'language': 'Lugha', 'x': 'jira_x', 'start': 'endesha', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'tuma_Orodha', 'payload': 'data_muhimu_data', 'proc': 'Mchakato', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'jina_jedwali', 'content': 'maudhui_thamani', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'faili_ingizo_jina', 'shell': 'sheli', 'color': '색상', 'transcript': '대화기록', 'offset': 'Chipua_thamani', 'h': '높이값', 'run': 'tekeleza_amri', 'c': 'msimbo_wa_kibambo', 'path': 'njia', 'encoding': 'seti_kibambo', 'end': 'tamatia_Chipua', 'ftp': 'faili_hamisha_muunganisho', 'pixels': '화소들', 'symbol': 'ishara_thamani', 'source': '원본자료', 'name': 'Jina', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
