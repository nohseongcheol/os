#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/예제시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'tshedimosetso', 'graphics_command': '그림명령', 'main': 'dirisa', 'row': '행위치', 'init': '초기값', 'target': 'setotwa', 'ROOT': '기준', 'text': 'SMS', 'binary': 'baenari', 'out': '결과자료', 'entry': 'tsenyo_ntlha', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'simolola_sethalo', 'col': '열위치', 'begin': 'simolola_Baya_ka_Tekatekanyo', 'kind': 'setlhopha_Boleng_4b6d6445', 'selector': 'setlhophi', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'sedirelwa', 'line': 'Mola', 'report': 'netefatso_pego', 'language': 'Puo', 'x': 'kgokagano_ya_x', 'start': 'dirisa', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'romela_lenaane', 'payload': 'selekanyo_sa_tshedimosetso_tshedimosetso', 'proc': 'Thulaganyo', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'leina_lenaneothalo', 'content': 'Diteng_Boleng', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'faele_tsenyo_leina', 'shell': 'setlhalosataelo', 'color': '색상', 'transcript': '대화기록', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'h': '높이값', 'run': 'diragatsa_Taelo', 'c': 'khoutuletshwao', 'path': 'tsela', 'encoding': 'Setlhophatshwao', 'end': 'kgaola_Baya_ka_Tekatekanyo', 'ftp': 'faele_fudusa_Kgolagano', 'pixels': '화소들', 'symbol': 'letshwao_Boleng', 'source': '원본자료', 'name': 'leina', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
