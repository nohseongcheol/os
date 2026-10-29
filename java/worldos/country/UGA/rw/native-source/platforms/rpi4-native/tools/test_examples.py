#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/예제시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'amakurushingiro', 'graphics_command': '그림명령', 'main': 'ihuriro', 'row': '행위치', 'init': '초기값', 'target': 'gusimbuza_igishya', 'ROOT': '기준', 'text': 'Umwandiko', 'binary': 'nyabibiri', 'out': '결과자료', 'entry': 'icyinjizwa_inota', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Itangira_igishushanyo', 'col': '열위치', 'begin': 'Itangira_Ofuseti', 'kind': 'icyiciro_agaciro', 'selector': 'muhitamo', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'umukiriya', 'line': 'umurongo', 'report': 'iyemeza_raporo', 'language': 'Ururimi', 'x': 'Ihuza_rya_x', 'start': 'ihuriro', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'kohereza_Urutonde', 'payload': 'ibitwarwa_amakurushingiro', 'proc': 'Inzira_a7054519', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'izina_imbonerahamwe', 'content': 'Ibirimo_agaciro', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'dosiye_icyinjizwa_izina', 'shell': 'insomamabwiriza', 'color': '색상', 'transcript': '대화기록', 'offset': 'Ofuseti_agaciro', 'h': '높이값', 'run': 'gukora_ibwiriza', 'c': '문자값', 'path': 'Inzira', 'encoding': 'itsinda_ry_inyuguti', 'end': 'kurangiza_Ofuseti', 'ftp': 'dosiye_iyimura_kwihuza', 'pixels': '화소들', 'symbol': 'ikimenyetso_agaciro', 'source': '원본자료', 'name': 'Izina', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
