#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/예제시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'datà', 'graphics_command': '그림명령', 'main': 'Bido', 'row': '행위치', 'init': '초기값', 'target': 'ebenlereanya', 'ROOT': '기준', 'text': 'SMS', 'binary': 'ndìnààbụọ', 'out': '결과자료', 'entry': 'ndebà_akara', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Mbido_osise', 'col': '열위치', 'begin': 'Mbido_Nnokwata', 'kind': 'otu_valuu_4b6d6445', 'selector': 'ihe_nhọpụta', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'klayènt', 'line': 'ahịrī', 'report': 'nkwèputaonòdù_akụkọ', 'language': 'Asụsụ', 'x': 'ngakọrịta_x', 'start': 'Bido', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'zìga_ndepụta', 'payload': 'ebe_mbulingwa_datà', 'proc': 'ùsòrò', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'akara_ahà_tebùl', 'content': 'ndịnà_valuu', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ọbọakwụkwọ_ndebà_akara_ahà', 'shell': 'nkọwannyemiwu', 'color': '색상', 'transcript': '대화기록', 'offset': 'Nnokwata_valuu', 'h': '높이값', 'run': 'mee_nnyemiwu', 'c': 'koòdù_nkeakàrà', 'path': 'ụzọ_ozi', 'encoding': 'òtù_mkpụrụedemede', 'end': 'mèdebe_Nnokwata', 'ftp': 'ọbọakwụkwọ_dògharịa_njikọ', 'pixels': '화소들', 'symbol': 'adimara_valuu', 'source': '원본자료', 'name': 'Aha', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
