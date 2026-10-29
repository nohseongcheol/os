#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/예제시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'imininingwane', 'graphics_command': '그림명령', 'main': 'Sebenzisa', 'row': '행위치', 'init': '초기값', 'target': 'impokophelo', 'ROOT': '기준', 'text': 'Itekisi', 'binary': 'unambambili', 'out': '결과자료', 'entry': 'okufakwayo_iphoyinti', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'qala_umdwebo', 'col': '열위치', 'begin': 'qala_I_ofisethi', 'kind': 'umunxa_inani', 'selector': 'isiqoki', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'iklayenti', 'line': 'umugqa', 'report': 'ukufakazisa_umbiko', 'language': 'Ulimi', 'x': 'okuxhumanisa_u_x', 'start': 'Sebenzisa', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'Thumela_Uhlu', 'payload': 'ukulayisha_okukhokhelwayo_imininingwane', 'proc': 'Inqubo', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'igama_ithebula', 'content': 'Okuqukethwe_inani', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ifayela_okufakwayo_igama', 'shell': 'isihumushi_miyalelo', 'color': '색상', 'transcript': '대화기록', 'offset': 'I_ofisethi_inani', 'h': '높이값', 'run': 'yenza_umyalo', 'c': 'ikhodi_yohlamvu', 'path': 'Indlela_2', 'encoding': 'iqoqo_lezinhlamvusimo', 'end': 'yekisa_I_ofisethi', 'ftp': 'ifayela_dlulisa_uxhumano', 'pixels': '화소들', 'symbol': 'uphawu_inani', 'source': '원본자료', 'name': 'Igama', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
