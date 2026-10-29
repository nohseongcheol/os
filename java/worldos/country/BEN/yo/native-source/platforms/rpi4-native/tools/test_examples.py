#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/예제시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'détà', 'graphics_command': '그림명령', 'main': 'Rọ́ọ̀nù', 'row': '행위치', 'init': '초기값', 'target': 'àfojúsùn', 'ROOT': '기준', 'text': 'SMS', 'binary': 'abèjì', 'out': '결과자료', 'entry': 'ìgbéwọlé_kókó', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'bẹ̀rẹ̀_íyàwòrán', 'col': '열위치', 'begin': 'bẹ̀rẹ̀_Ìtayọ', 'kind': 'ìsọ̀rí_iye', 'selector': 'olùyàn', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'aṣojú', 'line': 'ìlà', 'report': 'Àfọwọ́sí_ìjábọ̀', 'language': 'Èdè', 'x': 'ibi_ìtọ́kasí_x', 'start': 'Rọ́ọ̀nù', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'í_meèlì_Àtòkọ', 'payload': 'ojúlówó_détà_détà', 'proc': 'Ìlànà', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'orúkọ_atọ́ka', 'content': 'Àkóónú_iye', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fáìlì_ìgbéwọlé_orúkọ', 'shell': 'ṣẹ́ẹ̀lì', 'color': '색상', 'transcript': '대화기록', 'offset': 'Ìtayọ_iye', 'h': '높이값', 'run': 'ṣiṣẹ́_àṣẹ', 'c': 'kóòdù_ẹyọ_ọ̀rọ̀', 'path': 'ọ̀nà', 'encoding': 'àkójọpọ̀_ẹyọ_ọ̀rọ̀', 'end': 'parí_Ìtayọ', 'ftp': 'fáìlì_ṣàgbélọ_Ìsomọ́', 'pixels': '화소들', 'symbol': 'àmì_iye', 'source': '원본자료', 'name': 'Orúkọ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
