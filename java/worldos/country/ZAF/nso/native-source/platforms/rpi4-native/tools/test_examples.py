#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/예제시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'data', 'graphics_command': '그림명령', 'main': 'Diriša', 'row': '행위치', 'init': '초기값', 'target': 'nepo', 'ROOT': '기준', 'text': 'Sengwalwa', 'binary': 'paenari', 'out': '결과자료', 'entry': 'go_tsenya_tshedimošo_ntlha', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Thomišo_sethalwa', 'col': '열위치', 'begin': 'Thomišo_E_Šetšego', 'kind': 'legoro_boleng', 'selector': 'sekgethi', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'klaente', 'line': 'mothaladi', 'report': 'tiišetšo_pego', 'language': 'Polelo', 'x': 'kamano_ya_x', 'start': 'Diriša', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'Romela_Lenaneo', 'payload': 'morwalotefelwa_data', 'proc': 'tiragalo_a7054519', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'leina_tafola', 'content': 'Diteng_boleng', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'faele_go_tsenya_tshedimošo_leina', 'shell': 'šele', 'color': '색상', 'transcript': '대화기록', 'offset': 'E_Šetšego_boleng', 'h': '높이값', 'run': 'phethagatša_taelo', 'c': 'khouto_ya_tlhaka', 'path': 'Tsejana', 'encoding': 'sete_ya_ditlhaka', 'end': 'fetša_E_Šetšego', 'ftp': 'faele_fetišetša_kgokaganya', 'pixels': '화소들', 'symbol': 'leswao_boleng', 'source': '원본자료', 'name': 'Leina', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
